from django import template 

import hashlib
from six import text_type
from django.conf import settings
from django.contrib.auth.models import User

from asynther.models import LastUserVisit,Message
EDX_HOST = settings.EDX_HOST
register = template.Library()

@register.filter(name='lastmessagescount')
def lastmessagescount(self):
    last_visit = LastUserVisit.objects.filter(user__id=self).first()
    if last_visit:
        new_messages = Message.objects.all().filter(timestamp__gt=last_visit.last_visit)
        return new_messages.count()
    else:
        return 0;