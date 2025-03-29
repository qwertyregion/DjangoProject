from django.urls import path
from users_app import views

app_name = 'users_app'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path(r'activation_success/<uidb64>/<token>',
         views.activate_view, name='activation_success'),
    path(r'password_reset_confirm/<uidb64>/<token>',
         views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
