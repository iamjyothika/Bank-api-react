# Generated by Django 5.0.6 on 2024-07-13 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0004_transaction_receiver_transaction_reference_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='reference_number',
        ),
    ]
