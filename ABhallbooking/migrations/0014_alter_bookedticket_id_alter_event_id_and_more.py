# Generated by Django 5.1 on 2024-10-20 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ABhallbooking', '0013_bookedticket_payment_proof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedticket',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='seat',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
