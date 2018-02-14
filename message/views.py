from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import Profile
from .models import Message
from .forms import MessageForm


@login_required
def message_list(request):
    messages = request.user.profile.receiver_set.filter(receiver_visibility=True)
    ctx = {
        'messages': messages
    }
    return render(request, 'message_list.html', ctx)

def message_detail(request, pk):
    message = Message.objects.get(pk=pk)
    if not (message.sender == request.user.profile or message.receiver == request.user.profile):
        raise Http404('권한이 없습니다.')
    ctx = {
        'message': message,
    }
    return render(request, 'message_detail.html', ctx)

def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        if request.user.profile == message.receiver:
            message.receiver_visibility = False
            message.save()
            if not message.sender_visibility:
                message.delete()
            return redirect('message:messages')
        elif request.user.profile == message.sender:
            message.sender_visibility = False
            message.save()
            if not message.receiver_visibility:
                message.delete()
            return redirect('message:send_messages')
    else:
        raise Http404('잘못된 접근입니다.')

@login_required()
def send_message(request, username):
    message_form = MessageForm(request.POST or None)
    if request.method == 'POST':
        message = message_form.save(commit=False)
        receiver = User.objects.get(username=username).profile
        message.receiver = receiver
        message.sender = request.user.profile
        message.save()
        return redirect('message:send_messages')
    else:
        ctx = {'form': message_form, 'receiver': username}
        return render(request, 'message_send.html', ctx)


@login_required()
def send_message_list(request):
    messages = request.user.profile.sender_set.filter(sender_visibility = True)
    ctx = {
        'messages': messages,
    }
    return render(request, 'send_message_list.html', ctx)