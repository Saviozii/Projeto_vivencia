from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def aluno_home(request):
    return render(request,'supervisor_home.html')


@login_required
def supervisor_home(request):
    return render(request ,'supervisor_home.html')

