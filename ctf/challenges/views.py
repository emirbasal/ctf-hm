import os
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import FormView, View, ListView, DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, Http404
from .models import Challenge, ChallengeType
from .forms import ChallengeDetailForm
from users.models import Team, User


class TeamsChart:
    times_of_submitted_flags = []
    teams_dict = {}


line_chart = TeamsChart()


class ChallengeListView(ListView):
    model = ChallengeType
    template_name = 'challenges/challenges.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = 'Challenges'
        context['challenge_types'] = ChallengeType.objects.all()

        for challenge_type in context['challenge_types']:
            tmp_list = challenge_type.challenge_set.all()
            points_sum = tmp_list.aggregate(sum=Sum('points'))['sum']
            if points_sum is None:
                points_sum = 0
            challenge_type.points = points_sum
        return context


@method_decorator(login_required, name='dispatch')
class ChallengeDetailFormView(SingleObjectMixin, FormView):
    template_name = 'challenges/challenge_detail.html'
    form_class = ChallengeDetailForm
    model = Challenge

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()

        if request.user.team is None:
            messages.warning(request, 'You are not in a team. Join a team to submit flags')
            raise PermissionDenied('User %s is not in a team. Cant submit flags' % request.user)

        if request.user.team.done_challenges.filter(id=self.get_object().id).exists():
            messages.warning(request, 'This challenge was already successfully completed')
            raise PermissionDenied('User %s cant submit flag. Team %s already completed challenge' %
                                   (request.user, request.user.team))

        self.object = self.get_object()
        solution_flag = self.object.flag
        submitted_flag = request.POST['submitted_flag']
        if solution_flag == submitted_flag:
            request.user.points += self.object.points
            request.user.done_challenges.add(self.object)
            request.user.team.done_challenges.add(self.object)
            request.user.save()
            self.calculate_points_for_team(request.user.team)
            self.update_line_chart()

            messages.success(request, 'Submitted flag is right. Congratulations')
        else:
            messages.warning(request, f'Submitted flag is wrong')

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('challenge_detail', kwargs={'pk': self.object.pk})

    @staticmethod
    def calculate_points_for_team(team):
        tmp_list = team.user_set.all()
        points_sum = tmp_list.aggregate(sum=Sum('points'))['sum']
        if points_sum is None:
            points_sum = 0
        team.points = points_sum
        team.save()

    @staticmethod
    def update_line_chart():
        line_chart.times_of_submitted_flags.append(timezone.now())
        list_of_teams = Team.objects.all()
        for team in list_of_teams:
            if team.name not in line_chart.teams_dict:
                line_chart.teams_dict[team.name] = []
            line_chart.teams_dict[team.name].append(team.points)


class ChallengeDetailDetailView(DetailView):
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = self.get_object().title
        context['form'] = ChallengeDetailForm()
        # context['file'] = self.download(self.request, self.get_object().files.path)
        # challenge.team_set.all()
        return context


class ChallengeDetail(View):

    def get(self, request, *args, **kwargs):
        view = ChallengeDetailDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ChallengeDetailFormView.as_view()
        return view(request, *args, **kwargs)


def download(request, pk):
    challenge_file_path = Challenge.objects.get(pk=pk).files.path
    file_path = os.path.join(settings.MEDIA_ROOT, challenge_file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
