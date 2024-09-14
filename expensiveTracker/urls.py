from django.contrib import admin
from django.urls import path
from .views import home, register, user_login, user_logout, add_payment_method, add_transaction, transaction


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add-payment-method/', add_payment_method, name='add_payment_method'),
    path('add-transaction/', add_transaction, name='add_transaction'),
    path('transaction/<int:id>/', transaction, name='transaction'),
]
