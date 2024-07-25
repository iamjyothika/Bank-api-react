from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal



# {
#   "email":"sneha@gmail.com",
#   "username":"sneha",
#   "password":"sneha2001"
# }
# {
#   "email":"anusha@gmail.com",
#   "username":"anusha",
#   "password":"anusha07"
# # }
#  "email":"anusha@gmail.com",
#   "password":"anusha07#"
  #"new_password":"pranav@appu"
   #"new_password":"sneha$01
   #"password":"albin*10",




# # # Create your views here.
class SuperadminLoginView(APIView):
    permission_classes = [AllowAny]
    

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    
                })
            else:
                return Response({"detail": "Not a superadmin."}, status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class CustomerRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer=CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        print('Validation errors:',serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CustomerLoginView(APIView):
    permission_classes=[AllowAny]
    
    def post(self, request, *args, **kwargs):
        email= request.data.get("email")
        password = request.data.get("password")
        print(email,password)
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request,email=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    account = Account.objects.get(user=user)
                    balance = account.balance
                except Account.DoesNotExist:
                    balance = 0.00 
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'email': user.email,
                    'account_no': user.account_no,
                    'username':user.username,
                    'current_balance':balance
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Account is disabled."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Addbalance(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]  
    def get(self,request):
        balance=Account.objects.filter(user=request.user)
        serializer_obj=AccountSerializer(balance,many=True)
        return Response(serializer_obj.data,status=status.HTTP_200_OK) 
    def post(self,request):
        serializer=AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class Updatebalance(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def patch(self,request,id):
        account=get_object_or_404(Account,id=id,user=request.user)
        serializer=AccountSerializer(account,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
class CustomerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomerSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Customer information updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


class ListCustomer(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        if request.method == 'GET':
            customer = Customer.objects.all()
            serializer = CustomerSerializer(customer, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
  



class TransferFunds(APIView):
    def post(self, request, format=None):
        sender_account_id = request.data.get('sender_account')
        receiver_account_id = request.data.get('receiver_account')
        amount_str = request.data.get('amount')
        # transaction_type=request.data.get('transactiontype')
        amount = Decimal(amount_str)
        try:
            sender_account = Account.objects.get(pk=sender_account_id)
            receiver_account = Account.objects.get(pk=receiver_account_id)
        except Account.DoesNotExist:
            return Response({'error': 'One of the accounts does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if sender_account.balance < amount:
            return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a withdrawal transaction from sender's account
        Transaction.objects.create(
            account=sender_account,
            transaction_type='withdraw',
            amount=amount
        )

        # Create a deposit transaction for receiver's account
        Transaction.objects.create(
            account=receiver_account,
            transaction_type='deposit',
            amount=amount
        )

        # Adjust account balances
        sender_account.balance -= amount
        sender_account.save()

        receiver_account.balance += amount
        receiver_account.save()
        sender_customer = sender_account.user
        response_data = {
            'success': 'Funds transferred successfully.',
            'sender_account_name': sender_customer.username,
            'sender_account_number': sender_customer.account_no,
            'sender_remaining_balance': sender_account.balance
        }

        return Response(response_data, status=status.HTTP_200_OK)

 
class PerformTransaction(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        account_id = request.data.get('account_id')
        transaction_type = request.data.get('transaction_type')
        amount = request.data.get('amount')

        if transaction_type not in ['deposit', 'withdraw']:
            return Response({'error': 'Invalid transaction type.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Convert amount to float
            amount = Decimal(amount)
        except ValueError:
            return Response({'error': 'Invalid amount.'}, status=status.HTTP_400_BAD_REQUEST)
        if not account_id:
           
            account, created = Account.objects.get_or_create(user=request.user)

            # If it's a deposit transaction, process it
            if transaction_type == 'deposit':
                account.balance += amount
                account.save()

                # Create the transaction record
                Transaction.objects.create(
                    account=account,
                    transaction_type=transaction_type,
                    amount=amount
                )

                return Response({
                    'success': f'Funds deposited successfully.',
                    'previous_balance': account.balance - amount,
                    'new_balance': account.balance
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account not found. Create an account first.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            account = Account.objects.get(pk=account_id)
        except Account.DoesNotExist:
            return Response({'error': 'Account does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        previous_balance=account.balance 
        if transaction_type == 'withdraw':
            if account.balance < amount:
                return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)
            account.balance -= amount
        elif transaction_type == 'deposit':
            account.balance += amount

        account.save()

        # Create the transaction record
        Transaction.objects.create(
            account=account,
            transaction_type=transaction_type,
            amount=amount
        )

        return Response({
            'success': f'Funds {transaction_type}ed successfully.',
            'previous_balance': previous_balance,
            'new_balance': account.balance
        }, status=status.HTTP_200_OK)      




class ApplyLoanView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = response.data
      
        custom_response = {
            'loan_type': data['loan_type'],
            'customer': data['customer']['username'],  
            'amount': data['amountt'],
            'status': data['status']
        }
        return Response(custom_response, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])
def approve_or_reject_loan(request, pk):
    try:
        loan = Loan.objects.get(pk=pk)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)
    
    action = request.data.get('action') 
    if request.method == 'PATCH':
        if  action == 'approve':
            loan.status = 'Approved'  
        elif action == 'reject':
            loan.status = 'Rejected'  
        else:
            return Response({'error': 'Invalid operation for current status'}, status=status.HTTP_400_BAD_REQUEST)

        loan.save()
        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class Getloans(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self,request):
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans,many=True)
        data = serializer.data
        
        # Create a custom response
        custom_response = [
            {
                'id': loan['id'],
                'customer': loan['customer']['username'],  
                'loan_type': loan['loan_type'],
                'amountt': loan['amountt'],
                'status': loan['status']
            }
            for loan in data
        ]
        
        return Response(custom_response, status=status.HTTP_200_OK)
        
    
