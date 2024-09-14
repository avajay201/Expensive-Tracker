from django import forms
from .models import PaymentDetail, Transaction


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentDetail
        fields = ['method', 'upi', 'account_number']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user = user

        self.fields['upi'].widget.attrs['placeholder'] = 'Enter your UPI ID'
        self.fields['account_number'].widget.attrs['placeholder'] = 'Enter your Account(Name/Number)'
    
    def clean(self):
        cleaned_data = super().clean()
        upi = cleaned_data.get('upi')
        account_number = cleaned_data.get('account_number')

        if not upi and not account_number:
            raise forms.ValidationError("UPI or Account Number is required.")

        return cleaned_data

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', 'payment_method', 'to_account', 'location']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user = user
            self.fields['payment_method'].queryset = PaymentDetail.objects.filter(user=user)

        self.fields['location'].widget.attrs['hidden'] = True
        self.fields['amount'].widget.attrs['placeholder'] = 'Enter the transaction amount'
        self.fields['description'].widget.attrs['placeholder'] = 'Describe the transaction'
        self.fields['to_account'].widget.attrs['placeholder'] = 'Enter recipient account details'
        self.fields['location'].widget.attrs['placeholder'] = 'Enter location'

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount