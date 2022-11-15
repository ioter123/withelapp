# Generated by Django 4.1.3 on 2022-11-16 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=128, null=True, unique=True, verbose_name='아이디')),
                ('password', models.CharField(max_length=256, verbose_name='비밀번호')),
                ('name', models.CharField(max_length=128, verbose_name='이름')),
                ('nickname', models.CharField(max_length=128, verbose_name='닉네임')),
                ('phone', models.CharField(blank=True, max_length=128, null=True, verbose_name='연락처')),
                ('email', models.EmailField(blank=True, max_length=256, null=True, verbose_name='이메일')),
                ('birth', models.CharField(blank=True, max_length=256, null=True, verbose_name='생년월일')),
                ('address', models.CharField(blank=True, max_length=256, null=True, verbose_name='주소')),
                ('gender', models.CharField(blank=True, choices=[('M', '남자'), ('F', '여자')], max_length=20, null=True, verbose_name='성별')),
                ('introduce', models.CharField(blank=True, max_length=256, null=True, verbose_name='소개')),
                ('level', models.CharField(blank=True, choices=[('3', 'Lv3_미인증사용자'), ('2', 'Lv2_인증사용자'), ('1', 'Lv1_관리자'), ('0', 'Lv0_개발자')], max_length=20, null=True, verbose_name='등급')),
                ('auth', models.CharField(blank=True, max_length=10, null=True, verbose_name='인증번호')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='가입일')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='수정일')),
                ('last_login', models.DateTimeField(auto_now=True, null=True, verbose_name='마지막 로그인 날짜')),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_out', models.BooleanField(default=False, verbose_name='탈퇴여부')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '사용자',
                'verbose_name_plural': '사용자',
                'db_table': 'user',
            },
        ),
    ]
