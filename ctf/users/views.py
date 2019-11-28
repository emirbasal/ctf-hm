from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import ListView, FormView, View, CreateView, DetailView
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .forms import RegistrationForm, RegisterTeamForm, JoinTeamForm
from .models import Team, User
from challenges.views import line_chart


def user_register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(username=username, password=raw_password)
                login(request, account)
                messages.success(request, f'Account for {username} was successfully created')
                return redirect('home')
        else:
            form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})
    else:
        return redirect('profile')


@login_required
def user_profile(request):
    context = dict()
    context['headline'] = request.user.username
    return render(request, 'users/profile.html', context)


class TeamsRankingListView(ListView):
    model = Team
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = 'Home'
        context['teams'] = Team.objects.order_by('-points').values()
        context['teams_json'] = json.dumps(list(context['teams']), cls=DjangoJSONEncoder)
        context['line_chart'] = line_chart

        return context


class TeamsSummaryListAndCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = RegisterTeamForm
    template_name = 'users/teams.html'
    success_url = 'teams'

    def form_valid(self, form):
        self.object = form.save()
        self.object.user_set.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = 'Teams'
        context['teams'] = Team.objects.all()
        return context


class TeamDetailDetailView(DetailView):
    model = Team
    template_name = 'users/team_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = self.get_object().name
        context['form'] = JoinTeamForm()
        context['team_member'] = self.get_object().user_set.order_by('points')
        return context


class TeamDetailFormView(SingleObjectMixin, FormView):
    template_name = 'users/team_detail.html'
    form_class = JoinTeamForm
    model = Team

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object = self.get_object()
        submitted_password = request.POST['submitted_password']

        if submitted_password == self.object.password:
            self.object.user_set.add(request.user)
            messages.info(request, 'Team wurde erfolgreich beigetreten')
        else:
            messages.warning(request, 'Password ist inkorrect')

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('team_detail', kwargs={'pk': self.object.pk})


class TeamDetail(View):

    def get(self, request, *args, **kwargs):
        view = TeamDetailDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TeamDetailFormView.as_view()
        return view(request, *args, **kwargs)


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headline'] = self.get_object().username

        return context

