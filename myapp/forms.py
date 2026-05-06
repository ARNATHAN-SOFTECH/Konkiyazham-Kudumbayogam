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



from .models import Register, FamilyMember

class RegisterForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=FamilyMember.objects.all(),
        required=False,
        empty_label="Select Parent"
    )

    class Meta:
        model = Register
        fields = '__all__'


