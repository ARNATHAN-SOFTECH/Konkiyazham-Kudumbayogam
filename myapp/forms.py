from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Name',
            'required': True,
            'class': 'input-field'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email',
            'required': True,
            'class': 'input-field'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Your Message',
            'required': True,
            'class': 'textarea-field'
        })
    )



from .models import Register

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = "__all__"



