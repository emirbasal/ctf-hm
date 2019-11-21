from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, View, ListView, DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Challenge, ChallengeType
from .forms import ChallengeDetailForm

# from users.models import Team, User
from django.http import HttpResponse


# def home(request):
#     context = {
#         'users': User.objects.all(),
#         'teams': Team.objects.all(),
#         # 'points': Team.objects.all().count('points')
#     }
#
#     return render(request, 'challenges/home.html', context)


class ChallengeListView(ListView):
    model = ChallengeType
    template_name = 'challenges/challenges.html'
    # context_object_name = 'challenge_types'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenge_types'] = ChallengeType.objects.all()

        for challenge_type in context['challenge_types']:
            tmp_list = challenge_type.challenge_set.all()
            points_sum = tmp_list.aggregate(sum=Sum('points'))['sum']
            if points_sum is None:
                points_sum = 0

            challenge_type.points = points_sum

            #Sollte nicht immer bei dem aufruf gespeichert werden TODO:Change
            challenge_type.save()

        return context


@method_decorator(login_required, name='dispatch')
class ChallengeDetailFormView(SingleObjectMixin, FormView):
    template_name = 'challenges/challenge_detail.html'
    form_class = ChallengeDetailForm
    model = Challenge

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        if request.user.team.done_challenges.filter(id=self.get_object().id).exists():
            messages.warning(request, 'This challenge was already successfully completed')
            raise PermissionDenied('This challenge was already successfully completed')

        self.object = self.get_object()
        solution_flag = self.object.flag
        submitted_flag = request.POST['submitted_flag']
        if solution_flag == submitted_flag:
            request.user.points += self.object.points
            request.user.team.done_challenges.add(self.object)
            request.user.save()
            self.calculate_points_for_team(request.user.team)

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


class ChallengeDetailDetailView(DetailView):
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChallengeDetailForm()
        # challenge.team_set.all()
        return context


# @login_required
class ChallengeDetail(View):

    def get(self, request, *args, **kwargs):
        view = ChallengeDetailDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ChallengeDetailFormView.as_view()
        return view(request, *args, **kwargs)

