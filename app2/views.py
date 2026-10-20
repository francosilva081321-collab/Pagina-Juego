from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return render (request, 'app2/index.html')
def historia(request):
    return render(request, 'app2/historia.html')
def personajes(request):
    return render(request, 'app2/personajes.html')
def descarga(request):
    return render(request, 'app2/descarga.html')