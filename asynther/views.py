from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404,HttpResponse

from .models import Chat , Contact, Message,LastUserVisit
from django.conf import settings
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync
import datetime
User = get_user_model()


def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('timestamp').all()


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)



def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
def get_last_user_visit(self):
    return LastUserVisit.objects.filter(user=self).first()
@login_required(login_url="/accounts/login")
def index(request):

    get_last = get_last_user_visit(request.user)
    if get_last is not None:
        get_last.last_visit = datetime.datetime.now()
        get_last.save()
    else:
        get_last = LastUserVisit.objects.create(user=request.user)
        get_last.save()

    course_id = get_object_or_404(Chat.objects.order_by('?')[:1])

    course_id = course_id.id
    sidechats = Chat.objects.exclude(id=course_id)
    basechat = get_current_chat(course_id)
    messages = get_last_10_messages(course_id)
    return render(request, 'dashboard/mazeo/chat/chat.html', {
    
        'edx_host':settings.EDX_HOST,
        'sidechats':sidechats,
        'basechat': basechat,
        'messages': messages,
        'chat_id': id,

    })
@login_required(login_url="/accounts/login")
def room(request, course_id):
    
    get_last = get_last_user_visit(request.user)
    if get_last is not None:
        get_last.last_visit = datetime.datetime.now()
        get_last.save()
    else:
        get_last = LastUserVisit.objects.create(user=request.user)
        get_last.save()
    
    
    sidechats = Chat.objects.exclude(course__id=course_id)
    basechat = get_current_chat(course_id)
    messages = get_last_10_messages(course_id)
    return render(request, 'dashboard/mazeo/chat/chat.html', {
    
        'edx_host':settings.EDX_HOST,
        'sidechats':sidechats,
        'basechat': basechat,
        'messages': messages,
        'chat_id': id,

    })
    
@login_required(login_url="/accounts/login")
def filemessage(request):
    if request.method == 'POST':
        if request.FILES.get('send_file') != None:
            author = request.user;
            content = request.FILES['send_file'].name 
            file = request.FILES['send_file']
            yeni =  Message(author=author,content=content,file=file)
            yeni.save()
            current_chat = get_current_chat(request.POST['chatid'])
            current_chat.messages.add(yeni)
            current_chat.save()
        
            dt = yeni.timestamp
            layer = get_channel_layer()
            async_to_sync(layer.group_send)('chat_1', {
                'type': 'chat_message',
                'url': yeni.file.url,
                'message': content,
                'userid': request.user.username,
                'chatid': request.POST['chatid'],
                'timestamp': str(dt.strftime('%H:%M:%S')),
                })
            return HttpResponse('<p>Done</p>')
# #instructor
# @login_required(login_url="/accounts/login")
# def instructorindex(request):
    
#         teachman = True
#         course_id = Chat.objects.first()
#         course_id = course_id.id
#         sidechats = Chat.objects.exclude(id=course_id)
#         basechat = get_current_chat(course_id)
#         messages = get_last_10_messages(course_id)
#         return render(request, 'dashboard/instructor/chat/chat.html', {
#         'teachman': teachman,
#         'edx_host':settings.EDX_HOST,
#         'sidechats':sidechats,
#         'basechat': basechat,
#         'messages': messages,
#         'chat_id': id,

#     })
    