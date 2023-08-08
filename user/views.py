from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('login')  # 회원가입 성공 후 로그인 페이지로 이동

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)