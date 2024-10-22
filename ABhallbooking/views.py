# ABhallbooking/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import User, Event,BookedTicket, Payment
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import EventForm,PaymentForm
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserProfileForm, CustomPasswordChangeForm
from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from urllib.parse import quote

def index(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')  # Get the search query from the request
        if query:
            events = Event.objects.filter(name__icontains=query)  # Filter events based on the query
        else:
            events = Event.objects.all()  # Show all events if no query

        return render(request, 'index.html', {'user': request.user, 'events': events})
    
    return redirect('login')

def sign_up(request):
    if request.method == 'POST':
        email = request.POST['email']
        full_name = request.POST['full_name']
        student_id = request.POST['student_id']
        phone_number = request.POST['phone_number']  # New line
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        elif User.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already registered.')
        elif User.objects.filter(phone_number=phone_number).exists():  # New check
            messages.error(request, 'Phone number already registered.')
        else:
            user = User.objects.create_user(
                email=email, 
                full_name=full_name, 
                student_id=student_id, 
                phone_number=phone_number,  # New argument
                password=password
            )
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')

    return render(request, 'sign_up.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

# Helper function to check if the user is an admin
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    booked_seats = (
        BookedTicket.objects.filter(event=event).aggregate(total=Sum('seat_count'))['total'] or 0
    )
    available_seats = 100 - booked_seats  # Assuming 100 seats per event

    if request.method == 'POST':
        seat_count = int(request.POST['seat_count'])

        if seat_count > available_seats:
            messages.error(request, "Not enough seats available.")
        else:
            # Calculate total price
            total_price = Decimal(seat_count) * event.price_per_seat

            # Create BookedTicket
            booked_ticket = BookedTicket.objects.create(
                event=event,
                user=request.user,
                seat_count=seat_count,
                total_price=total_price
            )

            # Create Payment (initially unconfirmed)
            payment = Payment.objects.create(
                user=request.user,
                event=event,
                payment_method='PENDING',  # You can update this later when the user selects a payment method
                is_confirmed=False
            )

            # Store the booking details in the session
            request.session['booking_details'] = {
                'event_id': event.id,
                'seat_count': seat_count,
                'total_price': str(total_price),  # Convert Decimal to string for JSON serialization
                'booked_ticket_id': booked_ticket.id,
                'payment_id': payment.id
            }

            return redirect('payment', event_id=event.id)  # Redirect to payment page

    return render(request, 'book_event.html', {'event': event, 'available_seats': available_seats})

@login_required
def booked_tickets(request):
    if request.user.is_superuser:  # Check if the user is an admin
        tickets = BookedTicket.objects.all()  # Admin sees all tickets
    else:
        tickets = BookedTicket.objects.filter(user=request.user)  # Users see their own tickets

    return render(request, 'booked_tickets.html', {'tickets': tickets})

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(BookedTicket, id=ticket_id)  # No user filter for admins
    ticket.delete()
    messages.success(request, 'Ticket deleted successfully.')
    return redirect('booked_tickets')

def edit_event(request, event_id):
    if not request.user.is_staff:  # Ensure only admin can access
        return redirect('index')

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form, 'event': event})

@login_required
def payment_view(request, event_id):
    booking_details = request.session.get('booking_details')

    if not booking_details or booking_details['event_id'] != event_id:
        messages.error(request, "Invalid payment session. Please try again.")
        return redirect('index')

    event = get_object_or_404(Event, id=event_id)
    booked_ticket = get_object_or_404(BookedTicket, id=booking_details['booked_ticket_id'])
    payment = get_object_or_404(Payment, id=booking_details['payment_id'])

    if request.method == 'POST':
        payment_method = request.POST['payment_method']
        proof = request.FILES.get('proof_of_payment')

        if not proof:
            messages.error(request, "Please upload payment proof.")
        else:
            booked_ticket.payment_proof = proof
            booked_ticket.save()

            payment.payment_method = payment_method
            payment.proof_of_payment = proof
            payment.is_confirmed = True
            payment.save()

            del request.session['booking_details']
            messages.success(request, "Payment successful! Booking confirmed.")
            return redirect('booked_tickets')

    return render(request, 'payment.html', {
        'event': event,
        'booked_ticket': booked_ticket,
        'payment': payment,
        'booking_details': booking_details
    })
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
    else:
        messages.error(request, 'Invalid request method for deleting event.')
    return redirect('index')  # Or handle unauthorized access

def about_us(request):
    return render(request, 'about_us.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        
        if 'update_profile' in request.POST:
            if user_form.is_valid():
                user_form.save()
                message = quote("Your profile has been updated successfully.")
                return redirect(f'/update_profile/?message={message}')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                message = quote("Your password was successfully updated!")
                return redirect(f'/update_profile/?message={message}')
    else:
        user_form = UserProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })
@staff_member_required
def database_view(request):
    User = get_user_model()
    context = {
        'users': User.objects.all().values('id', 'email', 'full_name', 'student_id', 'is_superuser', 'is_staff'),
        'events': Event.objects.all(),
        'payments': Payment.objects.all(),
        'booked_tickets': BookedTicket.objects.all(),
    }
    return render(request, 'database.html', context)

@staff_member_required
def toggle_admin_status(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        User = get_user_model()
        user = User.objects.get(id=user_id)
        user.is_staff = not user.is_staff
        user.save()
        messages.success(request, f"Admin status for {user.email} has been {'granted' if user.is_staff else 'revoked'}.")
    return redirect('database')

@staff_member_required
def delete_database_item(request):
    item_type = request.GET.get('type')
    item_id = request.GET.get('id')

    if item_type == 'user':
        User.objects.filter(id=item_id).delete()
    elif item_type == 'event':
        Event.objects.filter(id=item_id).delete()
    elif item_type == 'payment':
        Payment.objects.filter(id=item_id).delete()
    elif item_type == 'ticket':
        BookedTicket.objects.filter(id=item_id).delete()

    return redirect('database')