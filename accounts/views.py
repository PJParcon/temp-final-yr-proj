from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from .forms import AccountDeletionForm, RegistrationForm, UsernameUpdateForm


def home(request):
    return render(request, 'accounts/home.html')


@require_http_methods(['GET', 'POST'])
def register(request):
    form = RegistrationForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('accounts:registration_complete')
    return render(request, 'accounts/register.html', {'form': form})


def registration_complete(request):
    return render(request, 'accounts/registration_complete.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
@require_http_methods(['GET', 'POST'])
def profile_update(request):
    form = UsernameUpdateForm(
        request.POST if request.method == 'POST' else None, instance=request.user
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your username has been updated.')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile_update.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def account_delete(request):
    form = AccountDeletionForm(
        request.user, request.POST if request.method == 'POST' else None
    )
    if request.method == 'POST' and form.is_valid():
        request.user.delete()
        logout(request)
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
    return render(request, 'accounts/account_delete.html', {'form': form})
