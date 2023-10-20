from django import forms
from django.core.validators import validate_email

def validate_email_field(value):
    try:
        validate_email(value)
        return True
    except:
        return False

class MailForm(forms.Form):
    email = forms.EmailField(validators=[validate_email_field],
                             error_messages={'invalid': 'Введите корректный адрес почты'})