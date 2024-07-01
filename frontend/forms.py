# frontend/forms.py

from django import forms
from .models import MensajeContacto

class ContactForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
