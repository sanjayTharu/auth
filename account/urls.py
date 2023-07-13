from django.urls import path
from account.views import RegistrationView,ActivateView,ActivationConfirm,GetCSRFToken

urlpatterns=[
    path('account/csrf_cookie',GetCSRFToken.as_view(),name='csrf_cookie'),
    path('account/registration/',RegistrationView.as_view(),name='register'),
    path('account/activate/<str:uid>/<str:token>/',ActivateView.as_view(),name='activate'),
    path('account/activate/',ActivationConfirm.as_view(),name='activation_confirm')
]