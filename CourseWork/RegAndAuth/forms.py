from django import forms

CHOICES = [('encrypt', 'encrypt'),
           ('decrypt', 'decrypt')]


class ShiphrForm(forms.Form):
    Mess = forms.CharField(max_length=250, required=True)
    Key = forms.CharField(max_length=250, required=True)
    EncryptedMessage = forms.CharField(max_length=250, required=False)
    Mess.widget.attrs.update({'placeholder': "Введите сообщение: "})
    Key.widget.attrs.update({'placeholder': "Введите ключ: "})
