from django.contrib import admin
from .models import PaymentMethod, PaymentDetail, Transaction


admin.site.register(PaymentMethod)
admin.site.register(PaymentDetail)

# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('amount', 'description', 'payment_method', 'to_account', 'transaction_time', 'location', 'payment_method', 'user')
#     list_filter = ('transaction_time', 'payment_method', 'user')
#     search_fields = ('amount', 'description', 'payment_method', 'to_account', 'user__username')

admin.site.register(Transaction)
