import threading
import time
import random

def clear_expired_codes():
    while True:
        # Удалить все одноразовые коды, срок действия которых истек
        OneTimeCode.objects.filter(created_at__lt=time.time() - 60).delete()
        time.sleep(60)  # Подождать 60 секунд перед очисткой снова

# Запустить функцию для очистки кодов в фоновом режиме
clear_codes_thread = threading.Thread(target=clear_expired_codes)
clear_codes_thread.daemon = True
clear_codes_thread.start()

def usual_login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        OneTimeCode.objects.create(code=random.choice('abcde'), user=user)
        # отправить одноразовый код на почту
        # перенаправь что-либо
    else:
        # верни 'неверный логин' сообщение об ошибке

def login_with_code_view(request):
    username = request.POST['username']
    code = request.POST['code']
    if OneTimeCode.objects.filter(code=code, user__username=username).exists():
        login(request, user)
    else:
        # ошибка
