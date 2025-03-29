from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.shortcuts import reverse
import logging
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.db import models

logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        if not password or len(password) < 8:
            raise ValueError('Пароль должен быть не короче 8 символов')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault('is_active', False)
        # extra_fields.is_active = False
        user.save(using=self._db)
        logger.info(f"Пользователь {email} успешно попал в базу данных")
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if 'first_name' not in extra_fields:
            raise ValueError('Имя (first_name) обязательно для суперпользователя')
        if 'last_name' not in extra_fields:
            raise ValueError('Имя (last_name) обязательно для суперпользователя')
        return self.create_user(email, password, **extra_fields)

    def activate_user(self, email):
        user = self.model.objects.get(email=email)
        user.is_active = True
        user.save(using=self._db)
        return user

    def get_active_users(self):
        return self.model.objects.filter(is_active=True)

    def get_by_phone(self, phone):
        return self.model.objects.get(phone=phone)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=15, blank=True, unique=True, verbose_name='псевдоним')
    email = models.EmailField(unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=False)
    # first_name = models.CharField(max_length=50, blank=True, verbose_name='имя')
    # last_name = models.CharField(max_length=50, blank=True, verbose_name='фамилия')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения', help_text='в формате 2006-10-25', )
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_absolut_url(self):
        return reverse('users_app:register', kwargs={})

# ------------------------------------------------------------------------------------------------------------

# class RegisteredUsers(models.Model):
#     first_name = models.CharField(max_length=15, verbose_name='введите имя', help_text='к примеру денис',
#                                   validators=(MaxLengthValidator(15, message='не борщщи'),
#                                               MinLengthValidator(3, message='не жадничай длинна более 2 символов'),
#                                               ),
#                                   )
#     last_name = models.CharField(max_length=15, verbose_name='введите фамилию', help_text='к примеру попов',
#                                  validators=(MaxLengthValidator(15, message='не борщщи'),
#                                              MinLengthValidator(3, message='не жадничай длинна более 2 символов'),
#                                              ),
#                                  )
#     nickname = models.CharField(max_length=20, unique=True, db_index=True, verbose_name='псевдоним', help_text='к примеру qwerty',
#                                 validators=(MaxLengthValidator(20, message='не борщщи'),
#                                             MinLengthValidator(3, message='не жадничай длинна более 2 символов'),
#                                             ),
#                                 )
#     photo = models.FileField(null=True, blank=True, verbose_name='фотография', name='photo_user',
#                              upload_to='photo_users/',
#                              )
#     birthday = models.DateField(verbose_name='день рождения', help_text='в формате 2006-10-25', )
#     email = models.EmailField(unique=True, db_index=True, verbose_name='электронная почта',
#                               help_text='к примеру qwertyregion05@mail.ru',
#                               )
#     password = models.CharField(max_length=8, db_index=True, verbose_name='пароль',
#                                 help_text='к примеру qwerty05 состоящий из 8 символов',
#                                 )
#     repeat_password = models.CharField(max_length=8, db_index=True, verbose_name='повторить пароль',
#                                        help_text='повторить пароль выше',
#                                        )
#
#     def __str__(self):
#         return self.nickname
#
#     def get_absolut_url(self):
#         return reverse('users:register_page', kwargs={})
