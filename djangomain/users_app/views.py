from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.edit import CreateView
from main_app import settings
from users_app.form import CustomUserCreationForm, CustomAuthenticationForm, ResetPasswordForm, ResetPasswordConfirmForm
from users_app.models import CustomUser


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users_app/register.html'

    def form_valid(self, form):
        with transaction.atomic():
            print("Форма валидна, сохраняем пользователя")
            user = form.save(commit=False)
            print(f"Пользователь сохранён: {user.email}")
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            print(f"Generated token: {token}")
            self._send_confirmation_email(user, form,  token)
        messages.success(self.request, "Регистрация прошла успешно! Пожалуйста, проверьте свою электронную"
                                       " почту для активации учетной записи.",)
        return HttpResponseRedirect(reverse("users_app:registration_success"))             # return super().form_valid(form)

    def form_invalid(self, form):
        print("Форма невалидна:", form.errors)
        messages.error(self.request, 'Account creation failed. Please try again.')
        return super().form_invalid(form)

    def _send_confirmation_email(self, user, form, token):
        print(f"User PK: {user.pk}")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        print(f"uid: {uid}")
        current_site = get_current_site(self.request)
        mail_subject = "Активируйте свой аккаунт"
        message = render_to_string(
            "users_app/activation_email.html",
            {
                "user": user,
                'username': user.username,
                'protocol': 'https' if self.request.is_secure() else 'http',
                "domain": current_site.domain,
                "uid": uid,
                "token": token,
            },
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = form.cleaned_data['email']
        email = EmailMultiAlternatives(mail_subject, message, from_email, to=[to_email])
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=False)
        print("token во время отправки: " + str(token))
        print("user во время отправки: " + str(user))


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users_app/login.html'
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('sait_app:home')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users_app/password_reset.html'
    form_class = ResetPasswordForm
    email_template_name = 'users_app/password_reset_email.html'
    success_url = reverse_lazy('users_app:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users_app/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users_app/password_reset_confirm.html'
    form_class = ResetPasswordConfirmForm
    success_url = reverse_lazy('users_app:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users_app/password_reset_complete.html'


def activate_view(request, uidb64, token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(id=user_id)
    except(TypeError, ValueError, OverflowError, ):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'users_app/activation_success.html')
    else:
        return render(request, 'users_app/activation_failed.html')


def registration_success(request):
    return render(request, 'users_app/registration_success.html')


# =====================================================================================================
# class RegisterView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'users/register.html'
#     success_url = reverse_lazy('users:registration_success')
#
#     def form_valid(self, form):
#         print("Форма валидна, сохраняем пользователя")
#         user = form.save()
#         print(f"Пользователь сохранён: {user.email}")
#         signer = TimestampSigner()
#         token = signer.sign(user.id)
#         activation_url = self.request.build_absolute_uri(reverse('users:activate', args=[token]))
#         send_mail(
#             'Подтвердите регистрацию',
#             f'Пожалуйста, подтвердите ваш email, перейдя по ссылке: {activation_url}',
#             None,
#             [user.email],
#             fail_silently=False,
#         )
#         response = super().form_valid(form)
#         return response
#
#     def form_invalid(self, form):
#         print("Форма невалидна:", form.errors)
#         return super().form_invalid(form)
#
# def activate_view(request, token):
#     signer = TimestampSigner()
#     try:
#         user_id = signer.unsign(token, max_age=86400)
#         user = CustomUser.objects.get(id=user_id)
#         if not user.is_active:
#             user.is_active = True
#             user.save()
#             return render(request, 'users/activation_success.html')
#         return render(request, 'users/already_activated.html')
#     except:
#         return render(request, 'users/activation_failed.html')
