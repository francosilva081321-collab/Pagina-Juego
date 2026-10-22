from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from .forms import InicioSesionForm, RegistroForm

def inicio(request):
    return render (request, 'app2/index.html')
def historia(request):
    return render(request, 'app2/historia.html')
def personajes(request):
    return render(request, 'app2/personajes.html')
def descarga(request):
    return render(request, 'app2/descarga.html')


class IniciarSesionView(LoginView):
    template_name = 'app2/login.html'
    authentication_form = InicioSesionForm


def registro(request):
    if request.user.is_authenticated:
        return redirect('hola')

    form = RegistroForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('hola')

    return render(request, 'app2/registro.html', {'form': form})