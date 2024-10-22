# forms.py
from django import forms
from .models import Event,Payment
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
# models.py or forms.py

TIME_CHOICES = [
    ("09:00", "9:00 AM"),
    ("10:00", "10:00 AM"),
    ("11:00", "11:00 AM"),
    ("12:00", "12:00 PM"),
    ("13:00", "1:00 PM"),
    ("14:00", "2:00 PM"),
    ("15:00", "3:00 PM"),
    ("16:00", "4:00 PM"),
    ("17:00", "5:00 PM"),
    ("18:00", "6:00 PM"),
    ("19:00", "7:00 PM"),
    ("20:00", "8:00 PM"),
    ("21:00", "9:00 PM"),
    ("22:00", "10:00 PM"),
    ("23:00", "11:00 PM"),
]

class EventForm(forms.ModelForm):
    start_time = forms.ChoiceField(choices=TIME_CHOICES)
    end_time = forms.ChoiceField(choices=TIME_CHOICES)

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'start_time', 'end_time', 'image','price_per_seat']

        widgets = {
            'date': forms.SelectDateWidget(),  # Dropdown for date
            'start_time': forms.Select(choices=TIME_CHOICES),  # Dropdown for start time
            'end_time': forms.Select(choices=TIME_CHOICES),  # Dropdown for end time
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'proof_of_payment']
    

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

User=get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'placeholder': 'Current Password'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'placeholder': 'New Password'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'})