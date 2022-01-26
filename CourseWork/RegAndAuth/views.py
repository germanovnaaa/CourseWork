from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import User
from .models import Message
from django.db.utils import IntegrityError
from django.contrib import messages
from .forms import ShiphrForm


def showRegHTML(request):
    return render(request, 'Registration/registration.html')


def signUpUser(request):
    try:
        if request.method == "POST":
            user = User()
            checkLogin = request.POST.get("username")
            checkPass = request.POST.get("pass")
            if len(checkLogin) > 4 and len(checkPass) > 4:
                user.Login = request.POST.get("username")
                user.Password = request.POST.get("pass")
                user.save()
                return HttpResponseRedirect("http://127.0.0.1:8000/encrypter")
            else:
                messages.error(request, 'Логин и пароль должны содержать более 4 символов')
                return redirect('http://127.0.0.1:8000/')
    except IntegrityError:
        messages.error(request, 'Пользователь с данным логином уже существует')
        return redirect('http://127.0.0.1:8000/')


def showEncrypterHTML(request):
    form = ShiphrForm()
    data = {
        'form': form
    }
    return render(request, 'Encrypter/encrypter.html', data)


def Encr(request):
    form = ShiphrForm(request.POST)
    if request.method == "POST" and form.is_valid():
        username = request.POST.get("Log")
        password = request.POST.get("pass")
        try:
            checkUserLogin = User.objects.get(Login=username, Password=password)
            if checkUserLogin is not None:
                msg = form.cleaned_data['Mess']
                key = form.cleaned_data['Key']
                mapped_key = text_and_key(msg, key)
                EncMes = shiphr_encryption(msg, mapped_key)
                tmp = Message.objects.create(EncryptMessage=EncMes, Mess=msg, UserId=checkUserLogin.id)
                messages.success(request, "Зашифрованное сообщение: "+EncMes)
                return HttpResponseRedirect("http://127.0.0.1:8000/encrypter")
        except User.DoesNotExist:
            messages.error(request, "Неверно введен логин или пароль")
            return HttpResponseRedirect("http://127.0.0.1:8000/encrypter")
    return HttpResponseRedirect("http://127.0.0.1:8000/encrypter")


def text_and_key(text, key):
    if text == '' or key == '':
        key_m = 'Error'
        return key_m
    else:
        key_m = ""
        j = 0
        for i in range(len(text)):
            if 1040 <= ord(text[i]) <= 1071:
                if j < len(key):
                    key_m += key[j].upper()
                    j += 1
                else:
                    j = 0
                    key_m += key[j].upper()
                    j += 1
            elif 1072 <= ord(text[i]) <= 1103:
                if j < len(key):
                    key_m += key[j]
                    j += 1
                else:
                    j = 0
                    key_m += key[j]
                    j += 1
            else:
                key_m += " "
        return key_m


def create_table():
    table = []
    for i in range(32):
        table.append([])
    for row in range(32):
        for column in range(32):
            if (row + 1040) + column > 1071:
                table[row].append(chr((row + 1040) + column - 32))
            else:
                table[row].append(chr((row + 1040) + column))
    return table


def create_table_1():
    table = []
    for i in range(32):
        table.append([])
    for row in range(32):
        for column in range(32):
            if (row + 1072) + column > 1103:
                table[row].append(chr((row + 1072) + column - 32))
            else:
                table[row].append(chr((row + 1072) + column))
    return table


def shiphr_encryption(message, mapped_key):
    table = create_table()
    table1 = create_table_1()
    enc_text = ""
    if mapped_key == 'Error':
        return enc_text
    for i in range(len(message)):
        # текст и ключ- заглавные
        if 1071 >= ord(message[i]) >= 1040:
            row = ord(message[i]) - 1040
            column = ord(mapped_key[i]) - 1040
            enc_text += table[row][column]
        # текст и ключ- строчные
        elif 1072 <= ord(message[i]) <= 1103:
            row = ord(message[i]) - 1072
            column = ord(mapped_key[i]) - 1072
            enc_text += table1[row][column]
        else:
            enc_text += message[i]
    return enc_text
