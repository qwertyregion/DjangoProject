from django import forms
from django.contrib.auth import authenticate
from django.core.validators import MaxLengthValidator, MinLengthValidator, ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm, PasswordResetForm
from users_app.models import CustomUser
# RegisteredUsers


class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
                                widget=forms.DateInput,
                                input_formats=("%Y-%m-%d", ),
                                help_text='в формате 2006-10-25',
                                label='день рождения',
                                error_messages={
                                                'required': 'без даты не получится',
                                                'invalid': 'не верный формат ',
                                               }
                                )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'birth_date', 'bio', )     # 'first_name', 'last_name',
        # widget = {
        #     'username': forms.CharField,
        #     'email': forms.EmailInput,
        #     'phone': forms.CharField,
        #     # 'birth_date': forms.DateInput,
        #     # 'password': forms.PasswordInput,
        #     # 'repeat_password': forms.PasswordInput,
        # }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # self.fields['first_name'].widget.attrs.update({
        #     'class': 'form-control',
        #     'placeholder': 'First Name',
        #     'required': 'False'
        # })
        # self.fields['last_name'].widget.attrs.update({
        #     'class': 'form-control',
        #     'placeholder': 'Last Name',
        #     'required': 'False'
        # })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'required': 'True'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
            'required': 'True'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'required': 'True'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Retype Password',
            'required': 'True'
        })

    def clean_email(self):
        cleaned_email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=cleaned_email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return cleaned_email

    def clean_username(self):
        cleaned_username = self.cleaned_data.get('username')
        count_username = CustomUser.objects.filter(username=cleaned_username)
        if len(count_username):
            # raise ValidationError('такой псевдоним занят выберите другой')
            self.add_error(field='username', error='такой псевдоним занят выберите другой')
        return cleaned_username


class CustomAuthenticationForm(AuthenticationForm):
    # email = forms.EmailField(label='email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    # def __init__(self, *args, **kwargs):
    #     super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
    #     self.fields['email'].widget.attrs.update({
    #         'class': 'form-control',
    #         'placeholder': 'email',
    #         'required': 'True'
    #     })
    #     self.fields['password'].widget.attrs.update({
    #         'class': 'form-control',
    #         'placeholder': 'Password',
    #         'required': 'True'
    #     })

    # def clean(self):
    #     email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #
    #     if email and password:
    #         self.user_cache = authenticate(self.request, username=email, password=password)
    #         if self.user_cache is None:
    #             raise forms.ValidationError(
    #                 self.error_messages['invalid_login'],
    #                 code='invalid_login',
    #                 params={'username': 'email'},
    #             )
    #         else:
    #             self.confirm_login_allowed(self.user_cache)
    #
    #     return self.cleaned_data


# -------------------------------------------------------------

class ResetPasswordForm(PasswordResetForm):
    class Meta:
        model = CustomUser
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email',
            'required': 'True'
        })


class ResetPasswordConfirmForm(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ResetPasswordConfirmForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New Password',
            'required': 'True'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Retype New Password',
            'required': 'True'
        })
