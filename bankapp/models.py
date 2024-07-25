import random
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Customer(AbstractUser):
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=30)
    id_proof=models.CharField(max_length=40)
    account_no=models.CharField(max_length=20)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 
    def save(self, *args, **kwargs):
        if not self.account_no:
            self.account_no = self.generate_account_no()
        super().save(*args, **kwargs)

    def generate_account_no(self):
        # Generate a random 12-digit account number
        return ''.join([str(random.randint(0, 9)) for _ in range(12)])

class Account(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE) 
    balance=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw')
       
    ]
    account=models.ForeignKey(Account,on_delete=models.CASCADE)
    transaction_type=models.CharField(max_length=10,choices=TRANSACTION_TYPE_CHOICES) 
    amount=models.DecimalField(max_digits=10,decimal_places=2)  
    date=models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transactions', null=True, blank=True)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions', null=True, blank=True)
    def __str__(self):
        return self.account.user.username

class Loan(models.Model):
    LOAN_TYPES=[
        ('Personal','Personal'),
        ('Home','Home'),
        ('Student','Student')
        
    ] 
    STATUS_CHOICES = [
        ('pending','pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected')
    ]
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    loan_type=models.CharField(max_length=20,choices=LOAN_TYPES)
    amountt=models.IntegerField()
    status=models.CharField(max_length=20,default="pending",choices=STATUS_CHOICES)

    def __str__(self):
        return self.customer.username
    

   
    





