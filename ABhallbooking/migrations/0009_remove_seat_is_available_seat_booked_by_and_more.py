# Generated by Django 5.1 on 2024-10-15 20:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ABhallbooking', '0008_alter_bookedticket_seat_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='is_available',
        ),
        migrations.AddField(
            model_name='seat',
            name='booked_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='seat',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-10-16 04:12:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seat',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seat',
            name='price',
            field=models.DecimalField(decimal_places=2, default=50.0, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seat',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='seat',
            name='seat_number',
            field=models.CharField(max_length=5),
        ),
    ]
