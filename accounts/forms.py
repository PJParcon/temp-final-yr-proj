from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name')


class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)
        field_classes = {'username': UsernameField}


class AccountDeletionForm(forms.Form):
    password = forms.CharField(
        label='Current password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError('Your current password is incorrect.')
        return password
