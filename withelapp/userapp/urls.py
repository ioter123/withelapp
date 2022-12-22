
from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'user'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('registerauth/', register_success, name='register_success'),
    path('agreement/', AgreementView.as_view(), name='agreement'),
    path('activate/<str:uid64>/<str:token>/', activate, name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('recovery/id/', RecoveryIdView.as_view(), name='recovery_id'),
    path('recovery/id/find/', ajax_find_id_view, name='ajax_id'),
    path('recovery/pw/', RecoveryPwView.as_view(), name='recovery_pw'),
    path('recovery/pw/find/', ajax_find_pw_view, name='ajax_pw'),
    path('recovery/pw/auth/', auth_confirm_view, name='recovery_auth'),
    path('recovery/pw/reset/', auth_pw_reset_view, name='recovery_pw_reset'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update_view, name='profile_update'),
    path('profile/password/', password_edit_view, name='password_edit'),
    path('profile/delete/', profile_delete_view, name='profile_delete'),
    # path('user_list', UserListView.as_view(), name='user_list'),
    # path('user_list/<int:pk>/', user_detail_view, name='user_detail'),
    # path('user_list/<int:pk>/edit/', user_edit_view, name='user_edit'),
    # path('user_list/<int:pk>/delete/', user_delete_view, name='user_delete'),

]