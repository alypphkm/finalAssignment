# ABhallbooking/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_event/', views.add_event, name='add_event'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('payment/<int:event_id>/', views.payment_view, name='payment'),
    path('booked-tickets/', views.booked_tickets, name='booked_tickets'),
    path('delete-ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('about-us/', views.about_us, name='about_us'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('database/', views.database_view, name='database'),
    path('delete-database-item/', views.delete_database_item, name='delete_database_item'),
    path('toggle_admin_status/', views.toggle_admin_status, name='toggle_admin_status'),
 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
