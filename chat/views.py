from django.shortcuts import render

# Create your views here.


def LoginView(request):
    return render(request, 'auth/login.html', context={})

