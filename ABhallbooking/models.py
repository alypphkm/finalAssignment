# ABhallbooking/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

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

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, student_id, phone_number, password=None):
        if not email:
            raise ValueError('The Email field is required')
        if not student_id:
            raise ValueError('The Student ID field is required')
        if not phone_number:
            raise ValueError('The Phone Number field is required')

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, student_id=student_id, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, student_id, phone_number, password=None):
        user = self.create_user(email, full_name, student_id, phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'student_id', 'phone_number']

    def __str__(self):
        return self.email

class Event(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    start_time = models.CharField(max_length=5, choices=TIME_CHOICES)
    end_time = models.CharField(max_length=5, choices=TIME_CHOICES)
    price_per_seat = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='event_images/')
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.create_seats()

    def create_seats(self, num_seats=100):  # Adjust the number of seats as needed
        for i in range(1, num_seats + 1):
            Seat.objects.create(event=self, seat_number=i)

    def __str__(self):
        return f"{self.name} - {self.date}"

class Seat(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Seat {self.seat_number} - {self.event.name}"

class BookedTicket(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat_count = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booked_date = models.DateTimeField(default=now)
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.event.name}"

class Payment(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key
    PAYMENT_METHODS = [
        ('QR', 'QR Payment'),
        ('BANK', 'Bank Transfer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    proof_of_payment = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.event.name} ({self.payment_method})"