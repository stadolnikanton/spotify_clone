from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label="Ваше имя:",
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.CharField(
        label="Электронная почта:",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label="Пароль:",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Подтвердите пароль:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data
