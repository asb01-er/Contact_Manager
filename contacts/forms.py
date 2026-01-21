from django import forms
from django.core.exceptions import ValidationError
from .models import Contact, User
from django.contrib.auth.forms import UserCreationForm

# Contact form
class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full','placeholder':'Contact Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input input-bordered w-full','placeholder':'Email Address'}))
    image = forms.FileField(required=False, widget=forms.FileInput(attrs={'class':'file-input file-input-bordered w-full','accept':'image/*'}))
    document = forms.FileField(required=False, widget=forms.FileInput(attrs={'class':'file-input file-input-bordered w-full','accept':'.pdf,.doc,.docx,.txt'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = self.initial.get('user')
        if Contact.objects.filter(user=user, email=email).exists():
            raise ValidationError("You already have a contact with this email.")
        return email

    class Meta:
        model = Contact
        fields = ('name','email','image','document')

# Sign Up form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
