from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import ContactForm, CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


@login_required
def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            return redirect('/thank-you/')

        return render(request, 'contact.html', {'form': form})

    form = ContactForm()
    return render(request, 'contact.html', {'form': form})
