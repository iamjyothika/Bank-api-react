from rest_framework import serializers
from .models import Customer,Account,Transaction,Loan
from django.contrib.auth.password_validation import validate_password

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('username', 'password', 'email','id_proof','phone')
    
    def create(self, validated_data):
        user = Customer(
            email=validated_data['email'],
            username=validated_data['username'],
            phone=validated_data['phone'],
            id_proof=validated_data['id_proof']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

      



class CustomerLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    class Meta:
        model=Customer
        fields=['email','password','account_no']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        user=serializers.StringRelatedField(read_only=True)
        model = Account
        fields =  ['balance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['account', 'transaction_type', 'amount']

class LoanSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Loan
        fields = ['id','customer','loan_type', 'amountt', 'status']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
        