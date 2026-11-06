
from django import forms
from .models import Register, FamilyMember


# ============================================================
# CUSTOM PARENT DROPDOWN
# ============================================================

class ParentChoiceField(forms.ModelChoiceField):

    NEW_VALUE = "__new__"

    def clean(self, value):

        self.is_new = value == self.NEW_VALUE

        if self.is_new:
            return None

        return super().clean(value)


# ============================================================
# CONTACT FORM
# ============================================================

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


# ============================================================
# REGISTRATION FORM
# ============================================================

class RegisterForm(forms.ModelForm):

    # --------------------------------------------------------
    # MOTHER
    # --------------------------------------------------------

    mother = ParentChoiceField(
        queryset=FamilyMember.objects.filter(
            gender='Female'
        ).order_by('name'),
        required=False,
        empty_label="-- Select Mother --",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'mother'
        })
    )

    mother_new_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'mother_new_name',
            'placeholder': 'Enter mother name'
        })
    )

    # --------------------------------------------------------
    # FATHER
    # --------------------------------------------------------

    father = ParentChoiceField(
        queryset=FamilyMember.objects.filter(
            gender='Male'
        ).order_by('name'),
        required=False,
        empty_label="-- Select Father --",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'father'
        })
    )

    father_new_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'father_new_name',
            'placeholder': 'Enter father name'
        })
    )

    # --------------------------------------------------------
    # CONFIRM PASSWORD
    # --------------------------------------------------------

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'confirm_password'
        })
    )

    class Meta:

        model = Register

        fields = '__all__'

    # ========================================================
    # FORM VALIDATION
    # ========================================================

    def clean(self):

        cleaned_data = super().clean()

        mother_field = self.fields['mother']
        father_field = self.fields['father']

        mother = cleaned_data.get('mother')
        father = cleaned_data.get('father')

        mother_new = mother_field.is_new
        father_new = father_field.is_new

        mother_new_name = (
            cleaned_data.get('mother_new_name') or ''
        ).strip()

        father_new_name = (
            cleaned_data.get('father_new_name') or ''
        ).strip()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # ----------------------------------------------------
        # MOTHER VALIDATION
        # ----------------------------------------------------

        if mother_new and not mother_new_name:

            self.add_error(
                'mother_new_name',
                'Please enter the mother name.'
            )

        # ----------------------------------------------------
        # FATHER VALIDATION
        # ----------------------------------------------------

        if father_new and not father_new_name:

            self.add_error(
                'father_new_name',
                'Please enter the father name.'
            )

        # ----------------------------------------------------
        # SAME PERSON VALIDATION
        # ----------------------------------------------------

        if mother and father and mother.pk == father.pk:

            raise forms.ValidationError(
                'Mother and Father cannot be the same person.'
            )

        if (
            mother_new
            and father_new
            and mother_new_name.casefold() == father_new_name.casefold()
        ):

            raise forms.ValidationError(
                'Mother and Father cannot have the same name.'
            )

        # ----------------------------------------------------
        # PASSWORD VALIDATION
        # ----------------------------------------------------

        if password and confirm_password:

            if password != confirm_password:

                self.add_error(
                    'confirm_password',
                    'Passwords do not match.'
                )

        # Store selection information for the registration view.
        cleaned_data['mother_is_new'] = mother_new
        cleaned_data['father_is_new'] = father_new

        return cleaned_data
