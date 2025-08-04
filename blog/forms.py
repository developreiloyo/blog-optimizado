from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre")
    email = forms.EmailField(label="Correo electrónico")
    mensaje = forms.CharField(widget=forms.Textarea, label="Mensaje")
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
