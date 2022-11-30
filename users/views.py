from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .models import User 
from .form import UserForm


def register(request):
    '''
    Register a new user
    '''
    template = 'register.html'
    if request.method == 'GET':
        print("this is register111111111111")
        return render(request, template, {'userForm':UserForm()})

    # POST
    userForm = UserForm(request.POST)
    if not userForm.is_valid():
        print("this is register2222222222222")
        return render(request, template, {'userForm':userForm})
    userForm.save()
    messages.success(request, '歡迎註冊')
    
    print("this is register3333333333333333")
    #return render(request, 'preference.html')
    return redirect('/')

def login(request):
    '''
    Login an existing user
    '''
    template = 'login.html'
    if request.method == 'GET':
        return render(request, template)

    # POST
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:    # Server-side validation
        messages.error(request, '請填資料')
        return render(request, template)

    user = authenticate(username=username, password=password)
    if not user:    # authentication fails
        messages.error(request, '登入失敗')
        return render(request, template)

    # login success
    auth_login(request, user)
    messages.success(request, '登入成功')
    return redirect('/')

def logout(request):
    '''
    Logout the user
    '''
    auth_logout(request)
    messages.success(request, '歡迎再度光臨')
    return redirect('/')

def selection(request):
    print("this is selection00000000")
    if request.method == 'GET':
        print("this is selection1111111111")
        return render(request, 'preference.html')

    if request.method == "POST":
        print("this is selection22222222222")
        #username = request.POST.get('user_name')
        #preference = request.POST.get('preference')
        user_name = request.POST["user_name"]
        preference = request.POST["preference"]
        return render(request, 'preference.html')
        #User.objects.filter(username = username).update(preference = preference)
        

        return redirect('/')

        
    print("this is selection333333333")
    return render(request, 'preference.html')
