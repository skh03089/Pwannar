from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.conf import settings

from .forms import SignUpForm, LoginForm, ProfileForm, SignUpProfileForm
from .models import Profile

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage



def MainPage(request):
    return render(request, 'mainpage.html')


def Create_User(request):
    signup_form = SignUpForm(request.POST or None)
    if request.method == 'POST':
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = signup_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        signup_form = SignUpForm()
    return render(request, 'signup.html', {'form': signup_form})


def SignIn(request):
    form = LoginForm(request, request.POST or None)
    ctx = {
        'form': form,
    }

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect('core:mainpage')
    if User.objects.filter(username=form.get_user()).exists():
        return redirect(reverse('accounts:confirm', kwargs={'username': form.get_user()}))
    return render(request, 'signin.html', ctx)


def SignOut(request):
    logout(request)
    return redirect(reverse('core:mainpage'))


def activate(request, uidb64, token):
    uidb64 = eval(uidb64)
    profile_form = SignUpProfileForm(request.POST or None, prefix='profile')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        HttpResponse('이메일 인증이 완료되었습니다.')
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
        return redirect('core:mainpage')
    else:
        return HttpResponse('Activation link is invalid!')



def myinfo(request, username):
    ctx = {
        'profile': get_object_or_404(Profile, user__username=username),
    }
    return render(request, 'myinfo.html', ctx)


def edit_myinfo(request):
    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.profile
    )
    if request.method == "POST" and form.is_valid():
        profile = form.save()
        return redirect(reverse(
            'accounts:myinfo',
            kwargs={'username': profile.user.username}
        ))

    ctx = {
        'form': form,
    }
    return render(request, 'edit_myinfo.html', ctx)

def confirm(request, username):
    if User.objects.filter(username=username, is_active=False).exists():
        ctx = {'username':username}
        return render(request, 'confirm.html', ctx)
    raise Http404('잘못된 경로입니다.')


def send_confirm_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your blog account.'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return HttpResponse('Please confirm your email address to complete the registration')

def resend(request, username) :
    if User.objects.filter(username=username, is_active=False).exists():
        return send_confirm_email(request, User.objects.get(username=username))
    raise Http404('잘못된 경로입니다.')