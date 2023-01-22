from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm  # CreationForm


class SignUp(CreateView):
    # form_class = CreationForm
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('forum:index')
    template_name = 'users/signup.html'