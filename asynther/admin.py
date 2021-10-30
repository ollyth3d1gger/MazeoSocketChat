from django.contrib import admin
from .models import Chat, Message
# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    
    list_display = ('id','title')
    list_per_page = 25

admin.site.register(Chat, ChatAdmin)
class MessagesAdmin(admin.ModelAdmin):
    
    list_display = ('id','author','content')
    list_per_page = 25

admin.site.register(Message, MessagesAdmin)