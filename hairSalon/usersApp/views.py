from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, FormView, CreateView, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from hairSalon.usersApp.forms import RegisterForm, LoginForm
from hairSalon.usersApp.models import AppUser


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = "profile.html"
    context_object_name = "user"

    def get_object(self):
        # Return the currently logged-in user
        return self.request.user


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = AppUser
    template_name = "edit_profile.html"
    fields = ["email", "first_name", "last_name"]
    success_url = reverse_lazy("profile")

    def get_object(self):
        # Ensure the user can only edit their own profile
        return self.request.user


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = AppUser
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        # Ensure the user can only delete their own profile
        return self.request.user


class LogInProfileView(FormView):
    template_name = "log-in.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Get the authenticated user from the form
        user = form.cleaned_data.get('user')

        # Log in the user
        login(self.request, user)
        return super().form_valid(form)


class RegisterProfileView(FormView):
    model = AppUser
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Save the new user
        user = form.save()

        # Log in the newly created user
        login(self.request, user)

        return super().form_valid(form)


class LogOutProfileView(View):
    def get(self, request, *args, **kwargs):
        # Render the confirmation page
        return render(request, 'log-out.html')

    def post(self, request, *args, **kwargs):
        # Log the user out
        logout(request)
        return HttpResponseRedirect(reverse('home'))
