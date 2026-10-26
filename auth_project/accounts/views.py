from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'auth/signup.html'


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'auth/base.html'
    login_url = reverse_lazy('login')
