from django import forms
from .models import UserModel


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'text', 'placeholder':'Email or Username'}),
                            label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password', 'placeholder': 'Password'}),
                               label='')


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'text', 'placeholder':'Email'}),
                             label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'text', 'placeholder': 'First Name'}),
                                 label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'text', 'placeholder': 'Last Name'}),
                                label='')
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'text', 'placeholder': 'State'}),
                                label='')
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'text', 'placeholder': 'City'}),
                                label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text', 'placeholder': 'Password'}),
                                label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'text', 'placeholder': 'Re-enter Password'}),
                                label='')

    class Meta:
        model = UserModel
        fields = ['email', 'first_name', 'last_name', 'state', 'city']

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Password must match!')
        return cleaned_data


class ChangePersonalDetailsForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'change-personal-details-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'change-personal-details-input'}), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'change-personal-details-input'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'change-personal-details-input'}))