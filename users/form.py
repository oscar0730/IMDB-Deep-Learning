from django import forms
from .models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': "register-content-text"}),)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': "register-content-text"}), )
    password2 = forms.CharField(label='ConfirmPw', widget=forms.PasswordInput(attrs={'class': "register-content-text"}),)
    email = forms.CharField(label='Email', max_length=128, widget=forms.TextInput(attrs={'class': "register-content-text"}),)
    age = forms.IntegerField(label='Age', widget=forms.TextInput(attrs={'class': "register-content-text"}),)
    #preferenece = forms.CharField(label='Preference', max_length=128, widget=forms.TextInput(attrs={'class': "register-content-text"}),)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'age']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password!=password2:
            raise forms.ValidationError('密碼不相符')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(user.password)
        if commit:
            user.save()
        return user

class PreferForm(forms.ModelForm):
    preferenece = forms.CharField()

    class Meta:
        model = User
        fields = ['preference']