from django.urls import path
from account.api.views import (
    registration_view,
    account_properties_view,
    update_account_view,
    ObtainAuthTokenView,
    does_account_exist_view,
    ChangePasswordView,
)

# important don't forget to put a backslash after the URL of a get request in Django as well as while calling via URL
app_name = 'account'

urlpatterns = [
    path('register', registration_view, name='register'),
    path('login', ObtainAuthTokenView.as_view(), name='login'),
    path('properties/', account_properties_view, name='properties'),
    path('properties/update', update_account_view, name='update'),
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
]

# while making a post request to the obtain_auth_token view remember to send 'username' as key instead of 'email' as
# shown below: 'username' = sansarya2121@gmail.com because we have overridden username by email in our account model

