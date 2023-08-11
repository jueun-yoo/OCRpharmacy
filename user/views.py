from supplements.models import Supplement
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserTotalIntake
from supplements.models import RecommendedIntake
from django.contrib import messages

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'user/index.html'
    context_object_name = 'supplements'

    def get_queryset(self):
        # 현재 로그인한 사용자가 등록한 영양제만 가져옴
        return Supplement.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
            # 부모 클래스의 get_context_data 호출
            context = super().get_context_data(**kwargs)
            # 현재 로그인한 사용자의 총 섭취량 가져오기
            context['total_intake'] = UserTotalIntake.objects.filter(user=self.request.user)
            return context

import logging

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('user:login')  # 회원가입 성공 후 로그인 페이지로 이동

    def form_valid(self, form):
        # 모든 필드가 제대로 채워졌는지 검사
        if form.is_valid():  # 이 부분이 폼의 유효성을 확인합니다.
            user = form.save()
            # 여기에서 필요한 경우 로그인 처리 등 추가 작업을 수행할 수 있습니다.
            return super().form_valid(form)
        else:
            return self.form_invalid(form) 
        
    def form_invalid(self, form):
        # 로깅을 위한 설정
        logger = logging.getLogger(__name__)
        logger.warning('회원가입 실패')
        for field, errors in form.errors.items():
            for error in errors:
                logger.warning(f"{field}: {error}")

        return super().form_invalid(form)
        
def root_redirect(request):
    User = get_user_model()
    if request.user.is_authenticated:
        return redirect('user:index')
    else:
        return redirect('user:login')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user:index')  # 로그인 성공 시 이동할 URL
            else:
                # 로그인 실패 시 오류 메시지 추가
                messages.error(request, '로그인 실패: 아이디 또는 비밀번호가 잘못되었습니다.')
                form = LoginForm()  # 폼을 비워서 다시 표시
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('user:login')