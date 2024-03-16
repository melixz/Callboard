import random
from string import hexdigits
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic.edit import CreateView
from callboard import settings
from .models import OneTimeCode
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:  # Проверка активности пользователя
            login(request, user)
            messages.success(request, ("You Have Been Logged In!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in. Please Try Again..."))
            return redirect('login')

    else:
        return render(request, "sign/templates/login.html", {})


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.is_active = False
            user.save()
            code = ''.join(random.sample(hexdigits, 6))
            # Отправка почты с OTP-кодом
            send_mail(
                subject='Код активации',
                message=f'Ваш код активации: {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            one_time_code = OneTimeCode(user=user, code=code)  # Указываем пользователя при создании объекта
            one_time_code.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Код был отправлен на вашу почту."))
            return redirect('code')
        return redirect('login')
    return render(request, 'sign/templates/signup.html', {'form': form})


def code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user = request.user
        if OneTimeCode.objects.filter(user__username=user.username, code=code).exists():
            # Проверка активации аккаунта
            #if not user.is_active:
            #    user.is_active = True
            #    user.save()
            return redirect('home')
        else:
            return render(request, 'sign/templates/code.html', {'message': 'Неверный код'})
    return render(request, 'sign/templates/code.html')


class InvalidCode(CreateView):
    template_name = 'sign/templates/invalid_code.html'


def LogoutViewCustom(request):
        logout(request)
        messages.success(request, ("You Have Been Logged Out."))
        return redirect('home')