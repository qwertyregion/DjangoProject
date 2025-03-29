from django.db import models
from django.urls import reverse
from django.core.validators import MaxLengthValidator, MinLengthValidator

STATUS_CHOICES = [
    ('low', 'низкийй'),
    ('medium', 'средни'),
    ('high', 'высокий'),
]


class AuthorManager(models.Manager):
    def info_author(self):
        return 'это информация о модели Author'


# ---------------------------------------------------------------
class Publisher(models.Model):
    publisher_name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=70, db_index=True, unique=True, default='', )
    popularity = models.CharField(max_length=6, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    publisher_content = models.TextField(default='text')

    def get_absolut_url(self):
        return reverse('sait_app:publisher_slug', kwargs={'publisher_slug': self.slug})


# ---------------------------------------------------------------
class Author(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='имя автора')
    last_name = models.CharField(max_length=30, verbose_name='фамилие автора')
    photo_author = models.FileField(verbose_name='фото автора', name='photo_author',
                                    upload_to='photo_author', null=True, blank=True, )
    slug = models.SlugField(max_length=70, db_index=True, unique=True, default='', verbose_name='слаг', )
    publisher = models.ManyToManyField("Publisher", related_name='author')
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name='author', null=True, blank=True, )

    objects_authormanager = AuthorManager()

    class Meta:
        base_manager_name = 'objects_authormanager'
        db_table = 'sait_app_author'
        default_related_name = 'author'
        ordering = ['-pk']
        verbose_name = 'писатель'
        verbose_name_plural = 'писатели'

    def __str__(self):
        return self.first_name

    def get_absolut_url(self):
        return reverse('sait_app:author_slug', kwargs={'author_slug': self.slug})


# ---------------------------------------------------------------
class Tag(models.Model):
    tag = models.CharField(max_length=100, )
    slug = models.SlugField(max_length=70, db_index=True, unique=True, default='', )

    def __str__(self):
        return self.tag

    def get_absolut_url(self):
        return reverse('sait_app:tag_slug', kwargs={'tag_slug': self.slug, })


# ---------------------------------------------------------------
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
#         return reverse('register_page', kwargs={})

# ----------------------------------------------------------------------------




