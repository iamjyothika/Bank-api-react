# Generated by Django 5.0.6 on 2024-07-15 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0007_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('Processed', 'Processed'), ('Approved', 'Approved')], default='pending', max_length=20),
        ),
    ]
