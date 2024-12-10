from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile.html"
    context_object_name = "user"

    def get_object(self):
        # Return the currently logged-in user
        return self.request.user


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "edit_profile.html"
    fields = ["email", "first_name", "last_name"]
    success_url = reverse_lazy("profile")

    def get_object(self):
        # Ensure the user can only edit their own profile
        return self.request.user


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        # Ensure the user can only delete their own profile
        return self.request.user
