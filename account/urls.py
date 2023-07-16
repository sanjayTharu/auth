from django.urls import path
from account.views import RegistrationView,ActivateView,ActivationConfirm,GetCSRFToken,LoginView,LogoutView,UserDetailView,ChangePasswordView

urlpatterns=[
    path('account/csrf_cookie',GetCSRFToken.as_view(),name='csrf_cookie'),
    path('account/registration/',RegistrationView.as_view(),name='register'),
    path('account/activate/<str:uid>/<str:token>/',ActivateView.as_view(),name='activate'),
    path('account/activate/',ActivationConfirm.as_view(),name='activation_confirm'),
    path('account/login/',LoginView.as_view(),name='login'),
    path('account/user/',UserDetailView.as_view(),name='detail'),
    path('account/change_password/',ChangePasswordView.as_view(),name='change_password'),
    path('account/logout/',LogoutView.as_view(),name='logout'),
]