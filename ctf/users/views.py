from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView, View, CreateView
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .forms import RegistrationForm, LoginAndRegisterTeamForm
from .models import Team


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
    #HIer muss nichts übergeben werden. Die Daten des angemeldeten Users sind immer verfügbar
    return render(request, 'users/profile.html')


class TeamsRankingListView(ListView):
    model = Team
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.order_by('-points').values()
        context['teams_json'] = json.dumps(list(context['teams']), cls=DjangoJSONEncoder)
        # context_json = json.dumps(context, cls=DjangoJSONEncoder)

        # for team in context['teams']:
        #     self.calculate_points_for_team(team)

        # return JsonResponse(context, safe=True)
        return context


class TeamsSummaryListAndCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = LoginAndRegisterTeamForm
    template_name = 'users/teams.html'
    success_url = 'teams'

    def form_valid(self, form):
        self.object = form.save()
        self.object.user_set.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        return context
