from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth

from django.urls import reverse
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


from django.contrib.auth.decorators import login_required
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/dashboard/chat')
        else:
            messages.error(request,'Kullanıcı Adı veya parola yanlış!')
            return redirect('login')
    else:

        return render(request, 'auth/login.html')

def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return redirect('index')

def signup(request):
    if request.method == 'POST':

        
        username = request.POST.get('username')
        username = username.upper().translate(str.maketrans({'Ğ':'G','Ş':'S','Ç':'C','Ö':'O','İ':'I','Ü':'U'}))
        special_characters = "!@#$%^&*()-+?_=,<>/:;'\\"
        username = username.replace(" ","")
        username = username.lower()
        if any(c in special_characters for c in username):
            messages.error(request,'Kullanıcı adı sadece harf ve sayılardan oluşmalıdır')
            return redirect(reverse('signup'))

        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if username == '':
            
            messages.error(request,'Bütün Alanların doldurulması Zorunludur')
            return redirect(reverse('signup'))
        if password == '':
            
            messages.error(request,'Bütün Alanların doldurulması Zorunludur')
            return redirect(reverse('signup'))
        
        if email  == '':
            messages.error(request,'Bütün Alanların doldurulması Zorunludur')
            return redirect(reverse('signup'))
        if password != password2:            
            messages.error(request,'Parolalar eşleşmiyor')
            return redirect(reverse('signup'))
        user = User.objects.create(username=username,email=email,password=make_password(password),is_active=1)
        user.save()
        messages.info(request,'Kayıt Başarılı lütfen giriş yapın')
        return redirect(reverse('login'))
    else:
        return render(request,'auth/register.html')




    if request.user.id == user_id:
        return render(request,'dashboard/student/profile/editprofile.html')