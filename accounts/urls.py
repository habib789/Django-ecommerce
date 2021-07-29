from django.urls import path
from .views import SignUp, ProfileView, ProfileUpdateView, ChangePass, user_order, user_order_details
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView,
                                       PasswordResetConfirmView, PasswordResetDoneView,
                                       PasswordResetCompleteView)

app_name = 'accounts'

urlpatterns = [
    # path('', Home.as_view(), name='home'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/<str:username>/', ProfileView.as_view(), name='profile_view'),
    path('profile/<int:pk>/<str:username>/update/', ProfileUpdateView.as_view(), name='update_info'),
    path('profile/change_password', ChangePass.as_view(), name='change_password'),
    path('profile/user_order', user_order, name='order_list'),
    path('profile/<int:pk>/user_order_details', user_order_details, name='order_details'),

    # RESET PASS
    path('profile/password_reset/', PasswordResetView.as_view(
        template_name="accounts/password_reset_form.html"), name='password_reset'),

    path('profile/password_reset_done/', PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"), name='password_reset_done'),

    path('profile/<uidb64>/<token>/password_reset_confirm/', PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),

    path('profile/password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
