from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from .models import User
from .models import Message
from django.db.utils import IntegrityError
from django.contrib import messages
from .forms import ShiphrForm
from django.core.files import File
import os


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
    form = ShiphrForm(request.POST, request.FILES or None)
    if request.method == "POST":
        username = request.POST.get("Log")
        password = request.POST.get("pass")
        mes = request.POST.get('mes')
        key = request.POST.get('key')
        try:
            checkUserLogin = User.objects.get(Login=username, Password=password)
            rb = request.POST.get("RB", None)
            if rb in ["Decrypt", "Encrypt"]:
                if rb == "Encrypt":
                    try:
                        ChosenFile = request.FILES['chosenFile']
                        chosenFile = ChosenFile.name
                        path = os.path.abspath(chosenFile)
                        chsFile = open(path, 'a')
                        myfile = File(chsFile)
                        if checkUserLogin is not None:
                            msg = mes
                            key = key
                            EncMes = encrypt(msg, key)
                            if EncMes == '':
                                data = {
                                    'username': username,
                                    'password': password,
                                    'mes': mes,
                                    'key': key,
                                    'result': EncMes
                                }
                                messages.error(request, "Некорректный ввод ключа или сообщения")
                                return render(request, "Encrypter/encrypter.html", data)
                            else:
                                data = {
                                    'username': username,
                                    'password': password,
                                    'mes': mes,
                                    'key': key,
                                    'result': EncMes
                                }
                                tmp = Message.objects.create(EncryptMessage=EncMes, UserId=checkUserLogin.id)
                                myfile.write("\nЗашифрованное сообщение: " + EncMes)
                                myfile.closed
                                messages.success(request, "Зашифрованное сообщение: " + EncMes)
                                return render(request, "Encrypter/encrypter.html", data)
                    except MultiValueDictKeyError:
                        data = {
                            'username': username,
                            'password': password,
                            'mes': mes,
                            'key': key,
                        }
                        messages.error(request, "Необходимо выбрать файл")
                        return render(request, "Encrypter/encrypter.html", data)
                elif rb == "Decrypt":
                    if checkUserLogin is not None:
                        msg = mes
                        key = key
                        try:
                            tmp = Message.objects.get(EncryptMessage=msg, UserId=checkUserLogin.id)
                            if tmp is not None:
                                EncMes = decrypt(msg, key)
                                data = {
                                    'username': username,
                                    'password': password,
                                    'mes': mes,
                                    'key': key,
                                    'result': EncMes
                                }
                                return render(request, "Encrypter/encrypter.html", data)
                        except Message.DoesNotExist:
                            data = {
                                'username': username,
                                'password': password,
                                'mes': mes,
                                'key': key,
                            }
                            messages.error(request, "Сообщение не найдено")
                            return render(request, "Encrypter/encrypter.html", data)
        except User.DoesNotExist:
            messages.error(request, "Неверно введен логин или пароль")
            return HttpResponseRedirect("http://127.0.0.1:8000/encrypter")
    return HttpResponseRedirect("http://127.0.0.1:8000/encrypter")


def encrypt(text, key):
    cyrillic_abc = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ,.!?1234567890@#$%^&*()_+:;/[]{}~`<>|"
    encrypted = ""
    for i in text:
        if i not in cyrillic_abc:
            return encrypted
    for i in key:
        if i not in cyrillic_abc:
            return encrypted
    if len(text) == 0 or len(key) == 0 or len(key) > len(text):
        return encrypted
    else:
        letter_to_index = dict(zip(cyrillic_abc, range(len(cyrillic_abc))))
        index_to_letter = dict(zip(range(len(cyrillic_abc)), cyrillic_abc))
        split_text = [
            text[i: i + len(key)] for i in range(0, len(text), len(key))
        ]

        for each_split in split_text:
            i = 0
            for letter in each_split:
                number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(cyrillic_abc)
                encrypted += index_to_letter[number]
                i += 1

        return encrypted


def decrypt(shiphr, key):
    cyrillic_abc = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ,.!?1234567890@#$%^&*()_+:;/[]{}~`<>|"
    decrypted = ""
    for i in shiphr:
        if i not in cyrillic_abc:
            return decrypted
    for i in key:
        if i not in cyrillic_abc:
            return decrypted
    if len(shiphr) == 0 or len(key) == 0:
        return decrypted
    else:
        letter_to_index = dict(zip(cyrillic_abc, range(len(cyrillic_abc))))
        index_to_letter = dict(zip(range(len(cyrillic_abc)), cyrillic_abc))
        split_encrypted = [
            shiphr[i: i + len(key)] for i in range(0, len(shiphr), len(key))
        ]

        for each_split in split_encrypted:
            i = 0
            for letter in each_split:
                number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(cyrillic_abc)
                decrypted += index_to_letter[number]
                i += 1

        return decrypted


def CheckMessagesInDB(request):
    if request.method == "POST":
        username = request.POST.get("Log")
        password = request.POST.get("pass")
        try:
            checkUserLogin = User.objects.get(Login=username, Password=password)
            if checkUserLogin is not None:
                MesUser = Message.objects.filter(UserId=checkUserLogin.id)
                return render(request, "CheckMessages/checkmessages.html", {"MesFromUser": MesUser})
            else:
                messages.error(request, "Неверно введен логин или пароль")
                return HttpResponseRedirect("http://127.0.0.1:8000/CheckMessages/")
        except User.DoesNotExist:
            messages.error(request, "Неверно введен логин или пароль")
            return HttpResponseRedirect("http://127.0.0.1:8000/CheckMessages/")
    return HttpResponseRedirect("http://127.0.0.1:8000/CheckMessages/")


def showCheckMessagesHTML(request):
    return render(request, 'CheckMessages/checkmessages.html')
