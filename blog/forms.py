from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class ContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={"rows": 6}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column(Field("name", placeholder="Your name"), css_class="col-md-6"),
                Column(Field("email", placeholder="you@example.com"), css_class="col-md-6"),
            ),
            Field("message", placeholder="How can I help you?"),
            "captcha",   # no Submit here; button will live in the template
        )