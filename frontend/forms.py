# frontend/forms.py

from django import forms
from .models import MensajeContacto
from .models import Credenciales

class ContactForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']



# frontend/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Credenciales

class CredencialesForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Credenciales
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CredencialesForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user