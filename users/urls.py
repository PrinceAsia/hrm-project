from django.urls import path

from users.views import (
    register_view,
    profile_view,
    update_account_view,
    change_password_view,
    # logout_view,
    reset_password_request_view,
    reset_password_confirm_view, delete_account_view
)

urlpatterns = [
    path('register/', register_view, name='register'),
    # path('logout/', logout_view, name='logout'),
    path('account/delete/', delete_account_view, name='delete_account'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_account_view, name='update_account'),
    path('password/change/', change_password_view, name='change_password'),
    path('password/reset/', reset_password_request_view, name='reset_password_request'),
    path('password/reset/confirm/', reset_password_confirm_view, name='reset_password_confirm'),
]
