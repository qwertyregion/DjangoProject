# from django import forms
# from django.core.validators import MaxLengthValidator, MinLengthValidator, ValidationError
# from fast_app1.models import RegisteredUsers
#
#
# class RegisterForm(forms.ModelForm):
#     birthday = forms.DateField(
#                                widget=forms.TextInput,
#                                input_formats=("%Y-%m-%d", ),
#                                help_text='в формате 2006-10-25',
#                                label='день рождения',
#                                error_messages={
#                                                'required': 'без даты не получится',
#                                                'invalid': 'не верный формат '
#                                               },
#                               )
#
#     class Meta:
#         model = RegisteredUsers
#         fields = ['first_name', 'last_name', 'nickname', 'photo_user', 'birthday', 'email', 'password', 'repeat_password', ]
#         widget = {
#             'first_name': forms.TextInput,
#             'last_name': forms.TextInput,
#             'nickname': forms.TextInput,
#             'photo_user': forms.FileInput,
#             'birthday': forms.DateInput,
#             'email': forms.EmailInput,
#             'password': forms.PasswordInput,
#             'repeat_password': forms.PasswordInput,
#         }
#         required = {
#             'photo_user': True,
#         }
#
#     def clean_photo_user(self):
#         cleaned_data = super().clean()
#         cleaned_photo = cleaned_data['photo_user']
#         if cleaned_photo is None:
#             self.add_error(field='photo_user', error='файл фотографии не выбран')
#         return cleaned_photo
#
#     def clean_nickname(self):
#         cleaned_data = super().clean()
#         cleaned_nickname = cleaned_data['nickname']
#         count_nickname = RegisteredUsers.objects.filter(nickname=cleaned_nickname)
#         if len(count_nickname):
#             # raise ValidationError('такой псевдоним занят выберите другой')
#             self.add_error(field='nickname', error='такой псевдоним занят выберите другой')
#         return cleaned_nickname
#
#     def clean_email(self):
#         cleaned_data = super().clean()
#         cleaned_email = cleaned_data['email']
#         count_email = RegisteredUsers.objects.filter(email=cleaned_email)
#         if len(count_email):
#             # raise ValidationError('эта почта уже зарегестрированна')
#             self.add_error(field='email', error='эта почта уже зарегестрированна')
#         return cleaned_email
#
#     def clean_repeat_password(self):
#         cleaned_data = super().clean()
#         cleaned_repeat_password = cleaned_data['repeat_password']
#         cleaned_password = cleaned_data['password']
#         if cleaned_repeat_password != cleaned_password:
#             self.add_error(field='repeat_password', error='вторичный пароль не соответствует первичному')
#         return cleaned_repeat_password


    # first_name = forms.CharField(
    #                              widget=forms.TextInput,
    #                              max_length=15,
    #                              min_length=3,
    #                              help_text='к примеру денис',
    #                              label='введите имя',
    #                              validators=[MaxLengthValidator(15, message='не борщщи'),
    #                                          MinLengthValidator(3, message='не жадничай длинна более 2 символов'),
    #                                          ],
    #                              error_messages={
    #                                              'min_length': 'не жадничай длинна более 2 символов',
    #                                              'required': 'без имени не получится',
    #                                             },
    #                             )
    #
    # last_name = forms.CharField(
    #                             widget=forms.TextInput,
    #                             max_length=15, min_length=3,
    #                             help_text='к примеру попов',
    #                             label='введите фамилие',
    #                             validators=[MaxLengthValidator(15, message='не борщщи'),
    #                                         MinLengthValidator(3, message='не жадничай длинна более 2 символов'),
    #                                         ],
    #                             error_messages={
    #                                 'min_length': 'не жадничай длинна более 2 символов',
    #                                 'required': 'без имени не получится',
    #                                            },
    #                            )
    #
    # nickname = forms.CharField(
    #                            widget=forms.TextInput,
    #                            max_length=20, min_length=5,
    #                            help_text='к примеру qwerty',
    #                            label='псевдоним',
    #                            )
    #
    # birthday = forms.DateField(
    #                            widget=forms.TextInput,
    #                            input_formats=("%Y-%m-%d", "%m/%d/%Y",  ),
    #                            help_text='в формате 2006-10-25',
    #                            label='день рождения',
    #                            error_messages={
    #                                            'required': 'без даты не получится',
    #                                           },
    #                           )
    #
    # email = forms.EmailField(
    #                          widget=forms.EmailInput,
    #
    #
    #                         )
    #
    # password = forms.CharField(
    #                            widget=forms.TextInput,
    #                            max_length=8,
    #                            min_length=8,
    #                            help_text='к примеру qwerty05 состоящий из 8 символов',
    #                            label='введите пароль',
    #                            )
    #
    # repeat_password = forms.CharField(
    #                                   widget=forms.TextInput,
    #                                   max_length=8,
    #                                   min_length=8,
    #                                   help_text='к примеру qwerty05 состоящий из 8 символов',
    #                                   label='повторите пароль',
    #                                   )
    # # widget = forms.PasswordInput,
    # class Meta:
    #     error_messages = {
    #                       'first_name': {
    #                                      'min_length': 'не жадничай длинна более 2 символов',
    #                                      'required': 'без имени не получится',
    #                                      },
    #                      }
    #
