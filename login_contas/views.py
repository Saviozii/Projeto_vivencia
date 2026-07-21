from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect('supervisor_home')
            else:
                return redirect('aluno_home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html')

