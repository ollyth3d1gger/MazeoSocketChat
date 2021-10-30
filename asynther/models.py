from django.contrib.auth import get_user_model
from django.db import models 

User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    author = models.ForeignKey(
        User,  on_delete=models.CASCADE,null=True)
    content = models.TextField()
    file = models.FileField(upload_to='media',null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Chat(models.Model):
    title = models.CharField(max_length=570,blank=True)
    chat_image = models.ImageField(upload_to='media/courses/',blank=True)
    
    participants = models.ManyToManyField(
        User,  blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)
class LastUserVisit(models.Model):
    user = models.ForeignKey(User,models.DO_NOTHING)
    last_visit = models.DateTimeField(auto_now_add=True)