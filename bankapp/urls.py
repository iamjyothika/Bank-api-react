from django.urls import path,include
from .views import *
urlpatterns = [
    path('login/',SuperadminLoginView.as_view(),name="superadminlogin"),
    path('register/',CustomerRegistrationView.as_view()),
    path('customerlogin/',CustomerLoginView.as_view()),
    path('updatepassword/',PasswordChangeView.as_view()),
    path('listcustomers/',ListCustomer.as_view()),
    path('balance/',Addbalance.as_view()),
    path('updatebalance/<int:id>',Updatebalance.as_view()),
    path('transfer/', TransferFunds.as_view(), name='transfer-funds'),
    path('transaction/',PerformTransaction.as_view()),
    path('loans/apply/', ApplyLoanView.as_view(), name='apply-loan'),
    path('loans/approve_reject/<int:pk>/', approve_or_reject_loan, name='approve-loan'),
    path('edit/',CustomerUpdateView.as_view()),
    path('loans/',Getloans.as_view())
   
   
]