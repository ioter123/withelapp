import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pathlib import Path
from .models import *
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .decorators import *
from django.core.exceptions import PermissionDenied
from .forms import *
from django.views.generic import CreateView, FormView, ListView
from django.utils.decorators import method_decorator
from .helper import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.core.serializers.json import DjangoJSONEncoder
from .helper import email_auth_num
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.shortcuts import get_object_or_404

EMAIL = getattr(settings, 'EMAIL', None)
SECRET_KEY = getattr(settings, 'SECRET_KEY', None)


class RegisterView(CreateView):
    model = User
    template_name = 'user/register.html'
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        self.request.session['register_auth'] = True
        messages.success(self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
        return reverse('register_success')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        send_mail(
            '{}님의 회원가입 인증메일 입니다.'.format(self.object.name),
            [self.object.user_id],
            html=render_to_string('user/register_email.html', {
                'user': self.object,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
                'domain': self.request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(self.object),
            }),
        )

        return redirect(self.get_success_url())


def register_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False

    return render(request, 'user/register_success.html')


@method_decorator(logout_message_required, name='dispatch')
class AgreementView(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False

        return render(request, 'user/agreement.html')

    def post(self, request, *args, **kwarg):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True

            return redirect('/register/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'user/agreement.html')


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('user_login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('user_login')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('user_login')


@method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = 'user/user_login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, user_id=user_id, password=password)

        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)
            remember_session = self.request.POST.get('remember_session', False)
            if remember_session:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('/user_login')


@method_decorator(logout_message_required, name='dispatch')
class RecoveryIdView(View):
    template_name = 'user/recovery_id.html'
    recovery_id = RecoveryIdForm

    def get(self, request):
        if request.method=='GET':
            form = self.recovery_id(None)
        return render(request, self.template_name, {'form_id':form})


def ajax_find_id_view(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    result_id = User.objects.get(name=name, phone=phone)

    return HttpResponse(json.dumps({"result_user_id": result_id.user_id}, cls=DjangoJSONEncoder),
                        content_type="application/json")


@method_decorator(logout_message_required, name='dispatch')
class RecoveryPwView(View):
    template_name = 'user/recovery_pw.html'
    recovery_pw = RecoveryPwForm

    def get(self, request):
        if request.method=='GET':
            form = self.recovery_pw(None)
            return render(request, self.template_name, {'form_pw':form})


def ajax_find_pw_view(request):
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    target_user = User.objects.get(user_id=user_id, name=name, phone=phone)

    if target_user:
        auth_num = email_auth_num()
        target_user.auth = auth_num
        target_user.save()

        send_mail(
            '비밀번호 찾기 인증메일입니다.',
            [user_id],
            html=render_to_string('user/recovery_email.html', {
                'auth_num': auth_num,
            }),
        )
    return HttpResponse(json.dumps({"result": target_user.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")


def auth_confirm_view(request):
    user_id = request.POST.get('user_id')
    input_auth_num = request.POST.get('input_auth_num')
    target_user = User.objects.get(user_id=user_id, auth=input_auth_num)
    target_user.auth = ""
    target_user.save()
    request.session['auth'] = target_user.user_id

    return HttpResponse(json.dumps({"result": target_user.user_id}, cls=DjangoJSONEncoder),
                        content_type="application/json")


@logout_message_required
def auth_pw_reset_view(request):
    if request.method == 'GET':
        if not request.session.get('auth', False):
            raise PermissionDenied

    if request.method == 'POST':
        session_user = request.session['auth']
        current_user = User.objects.get(email=session_user)
        login(request, current_user)

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)

        if reset_password_form.is_valid():
            user = reset_password_form.save()
            messages.success(request, "비밀번호 변경완료! 변경된 비밀번호로 로그인하세요.")
            logout(request)
            return redirect('user_login')
        else:
            logout(request)
            request.session['auth'] = session_user
    else:
        reset_password_form = CustomSetPasswordForm(request.user)

    return render(request, 'user/password_reset.html', {'form': reset_password_form})


@login_message_required
def profile_view(request):
    expiry_date = request.session.get_expiry_date()
    format = '%Y/%m/%d %H:%M:%S'
    expiry_date = expiry_date.strftime(format)
    if request.method == 'GET':
        return render(request, 'user/profile.html', {'expiry_date' : expiry_date})


@login_message_required
def profile_update_view(request):
    expiry_date = request.session.get_expiry_date()
    format = '%Y/%m/%d %H:%M:%S'
    expiry_date = expiry_date.strftime(format)
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            form = user_change_form.save(commit=True)
            form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return redirect('profile')
        return redirect('profile')
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        return render(request, 'user/profile_update.html', {'user_change_form':user_change_form, 'expiry_date' : expiry_date})


@login_message_required
def password_edit_view(request):
    expiry_date = request.session.get_expiry_date()
    format = '%Y/%m/%d %H:%M:%S'
    expiry_date = expiry_date.strftime(format)
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('profile')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(request, 'user/profile_password.html', {'password_change_form':password_change_form, 'expiry_date' : expiry_date})


@login_message_required
def profile_delete_view(request):
    expiry_date = request.session.get_expiry_date()
    format = '%Y/%m/%d %H:%M:%S'
    expiry_date = expiry_date.strftime(format)
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('/user_login/')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'user/profile_delete.html', {'password_form': password_form, 'expiry_date' : expiry_date})


# @method_decorator(admin_required, name='dispatch')
# class UserListView(ListView):
#     model = User
#     paginate_by = 10
#     template_name = 'user_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
#     context_object_name = 'user_list'        #DEFAULT : <model_name>_list
#
#     def get_queryset(self):
#         search_keyword = self.request.GET.get('q', '')
#         search_type = self.request.GET.get('type', '')
#         user_list = User.objects.order_by('-id')
#
#         if search_keyword:
#             if len(search_keyword) > 1:
#                 if search_type == 'all':
#                     search_user_list = user_list.filter(
#                         Q(user_id__icontains=search_keyword) | Q(name__icontains=search_keyword) | Q(
#                             phone__icontains=search_keyword))
#                 elif search_type == 'user_id_name':
#                     search_user_list = user_list.filter(
#                         Q(user_id__icontains=search_keyword) | Q(name__icontains=search_keyword))
#                 elif search_type == 'user_id':
#                     search_user_list = user_list.filter(user_id__icontains=search_keyword)
#                 elif search_type == 'name':
#                     search_user_list = user_list.filter(name__icontains=search_keyword)
#                 elif search_type == 'phone':
#                     search_user_list = user_list.filter(phone__icontains=search_keyword)
#
#                 return search_user_list
#             else:
#                 messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
#         return user_list
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = context['paginator']
#         page_numbers_range = 5
#         max_index = len(paginator.page_range)
#
#         page = self.request.GET.get('page')
#         current_page = int(page) if page else 1
#
#         start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
#         end_index = start_index + page_numbers_range
#         if end_index >= max_index:
#             end_index = max_index
#
#         page_range = paginator.page_range[start_index:end_index]
#         context['page_range'] = page_range
#
#         search_keyword = self.request.GET.get('q', '')
#         search_type = self.request.GET.get('type', '')
#
#         if len(search_keyword) > 1:
#             context['q'] = search_keyword
#         context['type'] = search_type
#
#         return context
#
#
# @admin_required
# def user_detail_view(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     context = {
#         'user': user,
#     }
#     return render(request, 'user/user_detail.html', context)
#
#
# @admin_required
# def user_edit_view(request, pk):
#     user = User.objects.get(id=pk)
#
#     if request.method == "POST":
#         form = AdminUserChangeForm(request.POST, instance=user)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             messages.success(request, "수정되었습니다.")
#             return redirect('/user_list/' + str(pk))
#     else:
#         user = User.objects.get(id=pk)
#         form = AdminUserChangeForm(instance=user)
#         context = {
#             'user_change_form': form,
#             'edit': '수정하기',
#         }
#         return render(request, "user/user_edit.html", context)
#
#
# @admin_required
# def user_delete_view(request, pk):
#     user = User.objects.get(id=pk)
#     user.delete()
#     messages.success(request, "삭제되었습니다.")
#     return redirect('/user_list/')
