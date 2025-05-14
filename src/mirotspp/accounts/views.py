from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm, LoginForm
from django.contrib.auth.views import LoginView as DjangoLoginView


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')


class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('profile')


@login_required
def profile(request):
    context = {
        'user': request.user,
        'title': 'Мой профиль'
    }
    return render(request, 'accounts/profile.html', context=context)
