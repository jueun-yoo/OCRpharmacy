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
from supplements.models import RecommendedIntake, RecommendedNutrient
from django.contrib import messages

#퍼센트 계산
def calculate_intake_percentage(user):
    intake_percentages = {}
    #사용자의 총섭취량 데이터 가져오기
    user_intakes = UserTotalIntake.objects.filter(user=user)
    #사용자의 적정섭취량 데이터 가져오기
    recommended_intakes = {r.nutrient.name: r.dosage for r in RecommendedNutrient.objects.filter(recommended_intake=user.recommended)}

    for intake in user_intakes:
        nutrient_name = intake.nutrient.name
        actual_dosage = intake.dosage
        recommended_dosage = recommended_intakes.get(nutrient_name)

        if recommended_dosage:
            percentage = (actual_dosage / recommended_dosage) * 100
            intake_percentages[nutrient_name] = percentage
        else:
            intake_percentages[nutrient_name] = None

    return intake_percentages


def index_view(request):
    # 로그인되어 있지 않은 사용자에 대해 로그인 페이지로 리디렉션
    if not request.user.is_authenticated:
        return redirect('login')

    supplements = Supplement.objects.filter(user=request.user)
    total_intake = UserTotalIntake.objects.filter(user=request.user)
    intake_percentages = calculate_intake_percentage(request.user)

    return render(request, 'user/index.html', {
        'supplements': supplements,
        'total_intake': total_intake,
        'intake_percentages': intake_percentages
    })

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