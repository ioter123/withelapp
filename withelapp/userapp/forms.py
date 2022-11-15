from django import forms
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, SetPasswordForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model


def phone_validator(value):
    if len(str(value)) != 10:
        raise forms.ValidationError('정확한 핸드폰 번호를 입력해주세요.')


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False
        })
        self.fields['password1'].label = '비밀번호 확인'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['password2'].label = '비밀번호'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['nickname'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['birth'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['address'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['gender'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['introduce'].label = '소개'
        self.fields['introduce'].widget.attrs.update({
            'class': 'form-control',
        })

    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2','name', 'nickname', 'phone', 'email', 'birth', 'address', 'gender', 'introduce']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.level = '2'
        user.save()
        user.is_active = False
        return user


class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', }),
        error_messages={'required': '아이디를 입력해주세요.'},
        label='아이디'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', }),
        error_messages={'required': '비밀번호를 입력해주세요.'},
        label='비밀번호'
    )

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')

        if user_id and password:
            try:
                user = User.objects.get(email=user_id)
            except User.DoesNotExist:
                self.add_error('email', '아이디가 존재하지 않습니다.')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')


class RecoveryIdForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput,)
    phone = forms.CharField(widget=forms.TextInput,)

    class Meta:
        fields = ['name', 'phone']

    def __init__(self, *args, **kwargs):
        super(RecoveryIdForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'form_name',
        })
        self.fields['phone'].label = '연락처'
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'id': 'form_phone'
        })


class RecoveryPwForm(forms.Form):

    user_id = forms.CharField(
        widget=forms.TextInput, )
    name = forms.CharField(
        widget=forms.TextInput,)
    phone = forms.CharField(
        widget=forms.TextInput, )

    class Meta:
        fields = ['user_id', 'name', 'phone']

    def __init__(self, *args, **kwargs):
        super(RecoveryPwForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_email',
        })
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_name',
        })
        self.fields['phone'].label = '연락처'
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'id': 'pw_form_phone',
        })


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })


class CustomUserChangeForm(UserChangeForm):
    password = None

    name = forms.CharField(label='이름', widget=forms.TextInput(
        attrs={'class': 'form-control', }),
    )
    nickname = forms.CharField(label='닉네임', widget=forms.TextInput(
        attrs={'class': 'form-control', }),
    )
    phone = forms.CharField(label='연락처', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '11', 'oninput': "maxLengthCheck(this)", }),
    )
    email = forms.EmailField(label='이메일', widget=forms.EmailInput(
        attrs={'class': 'form-control', }),
    )

    birth = forms.CharField(label='생년월일', widget=forms.TextInput(
        attrs={'class': 'form-control',}),
    )
    address = forms.CharField(label='주소', widget=forms.TextInput(
        attrs={'class': 'form-control',}),
    )
    gender = forms.CharField(label='성별', widget=forms.TextInput(
        attrs={'class': 'form-control', }),
                           )
    introduce = forms.CharField(label='소개', widget=forms.TextInput(
        attrs={'class': 'form-control', }),
    )

    class Meta:
        model = User()
        fields = ['name', 'nickname', 'phone', 'email', 'birth', 'address', 'gender', 'introduce']


# class AdminUserChangeForm(UserChangeForm):
#     password = None
#     name = forms.CharField(label='이름', widget=forms.TextInput(
#         attrs={'class': 'form-control', }),
#                            )
#     nickname = forms.CharField(label='닉네임', widget=forms.TextInput(
#         attrs={'class': 'form-control', }),
#                                )
#     phone = forms.CharField(label='연락처', widget=forms.TextInput(
#         attrs={'class': 'form-control', 'maxlength': '11', 'oninput': "maxLengthCheck(this)", }),
#                             )
#     email = forms.EmailField(label='이메일', widget=forms.EmailInput(
#         attrs={'class': 'form-control', }),
#                              )
#
#     birth = forms.CharField(label='생년월일', widget=forms.TextInput(
#         attrs={'class': 'form-control', }),
#                             )
#     address = forms.CharField(label='주소', widget=forms.TextInput(
#         attrs={'class': 'form-control', }),
#                               )
#     gender = forms.CharField(label='성별', widget=forms.TextInput(
#         attrs={'class': 'form-control', }),
#                              )
#     introduce = forms.CharField(label='소개', widget=forms.TextInput(
#         attrs={'class': 'form-control', }),
#                                 )
#
#     class Meta:
#         model = User()
#         fields = ['name', 'nickname', 'phone', 'email', 'birth', 'address', 'gender', 'introduce', 'is_admin', 'is_out']


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })


class CheckPasswordForm(forms.Form):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control', }),
                               )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password

        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')

