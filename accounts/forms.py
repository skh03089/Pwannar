from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    )
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('이미 가입된 이메일 입니다.')
        return email


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': ("아이디 또는 비밀번호가 틀렸습니다."
                          ),
        'inactive': "이메일 인증을 완료해주세요 <buttton>이메일 재전송</button>",
    }

    class Meta:
        model = User
        fields = ['username', 'password']


class SignUpProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'image',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


