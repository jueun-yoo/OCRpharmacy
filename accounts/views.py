from django.shortcuts import render, redirect
from .forms import SignUpForm

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # 회원가입 성공 시 이동할 URL (success 페이지 등)
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

