from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from src.account.api.serialisers import RegistrationSerializer, AccountPropertiesSerializer, ChangePasswordSerializer
from src.account.models import Account
from rest_framework.views import APIView
from django.contrib.auth import authenticate


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    if request.method == 'POST':
        data = {}
        email = request.data.get('email', '0').lower()
        if validate_email(email) != None:
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return Response(data)

        username = request.data.get('username', '0')
        if validate_username(username) != None:
            data['error_message'] = 'That username is already in use.'
            data['response'] = 'Error'
            return Response(data)

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
            data['pk'] = account.pk
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


def validate_email(email):
    account = None
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email


def validate_username(username):
    account = None
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def account_properties_view(request):
    try:
        print('ehat the fuck')
        account = request.user
    except Account.DoesNotExist:
        print('what the fuck 2')
        content = {'message': 'what the fuck man'}
        return Response(status=status.HTTP_404_NOT_FOUND, data=content)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountPropertiesSerializer(account, data=request.data)
        api_response = {}
        if serializer.is_valid():
            serializer.save()
            api_response['messgae'] = 'Account updated successfully'
            return Response(data=api_response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# note that u cant change the primary key of a record with a PUT request


class ObtainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        email = request.POST.get('email')
        password = request.POST.get('password')

        account = authenticate(email=email, password=password)
        api_response = {}
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)

            api_response['response'] = 'Successfully authenticated'
            api_response['email'] = account.email.lower()
            api_response['pk'] = account.pk
            api_response['token'] = token.key
        else:
            api_response['response'] = 'Error'
            api_response['error_message'] = 'Invalid credentials'
        return Response(api_response)


@api_view(['GET', ])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):
    if request.method == 'GET':
        email = request.GET['email'].lower()
        data = {}
        try:
            account = Account.objects.get(email=email)
            data['response'] = email
        except Account.DoesNotExist:
            data['response'] = "Account does not exist"
        return Response(data)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # confirm the new passwords match
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"response": "successfully changed password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
