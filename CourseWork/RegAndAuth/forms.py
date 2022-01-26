from django import forms


class ShiphrForm(forms.Form):
    Mess = forms.CharField(max_length=250, required=False)
    Key = forms.CharField(max_length=250, required=False)
    EncryptedMessage = forms.CharField(max_length=250, required=False)
    Mess.widget.attrs.update({'placeholder': "Введите сообщение "})
    Key.widget.attrs.update({'placeholder': "Введите ключ "})
