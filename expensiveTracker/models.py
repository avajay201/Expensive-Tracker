from django.db import models
from django.contrib.auth.models import User


class PaymentMethod(models.Model):
    METHOD_CHOICES = [
        ('UPI', 'UPI'),
        ('Bank Account', 'Bank Account'),
    ]

    method = models.CharField(max_length=20, choices=METHOD_CHOICES)

    def __str__(self):
        return self.method

class PaymentDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    upi = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.method} - {self.upi if self.upi else self.account_number}'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    payment_method = models.ForeignKey(PaymentDetail, on_delete=models.CASCADE)
    to_account = models.CharField(max_length=255)
    transaction_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} : Rs.{self.amount}'
