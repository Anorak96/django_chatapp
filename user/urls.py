from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'
urlpatterns = [
    path('token', views.LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.AccountView.as_view(), name='account'),
]