from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, correoForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def home (request):
    return render (request, 'home.html')

#@csrf_exempt
def signup (request):
    
    if request.method == 'GET':
        return render (request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST ['password1'] == request.POST ['password2']:
            try:
                #usuario registrado
                user  = User.objects.create_user( username =request.POST ['username'], password=request.POST['password1'] )
                user.save()
                login (request, user)
                return redirect ('analisis')
            except IntegrityError:
                return render (request, 'signup.html', {
                'form': UserCreationForm,
                'error':"El usuario ya existe"
                })
        return render (request, 'signup.html', {
            'form': UserCreationForm,
            "error":"contraseñas no coinciden"
        })
        
def tasks (request):
    return render (request, 'tasks.html')

def create_task (request):
    return render (request, 'create_task.html', {
        'form':TaskForm
    })

@login_required
def signout (request):
    logout(request)
    return redirect ('home')

#@csrf_exempt
def singin (request):
    if request.method == 'GET':
        return render (request, 'singin.html', {
        'form':AuthenticationForm
        })
    else:
        user = authenticate(request, username = request.POST['username'], password=request.POST['password'])
        if user is None:
            return render (request, 'singin.html', {
                'form':AuthenticationForm, 
                'error':'usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('analisis')
        
#@csrf_exempt
@login_required
def send_mail (mail) :
    print (mail)
    context = {'mail':mail}
    template = get_template ("palcorreo.html")
    content = template.render (context)
    
    email = EmailMultiAlternatives (
    'Analisis de notas',
    'sale left',
    settings.EMAIL_HOST_USER,
    [mail]
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    
#@csrf_exempt
@login_required
def correo (request):
   
   #METODO UNO PERO ANTIGUO PARA LLENAR TABLAS
    #print (request.GET['name'])#METODO GET para obtener los datos a travez de la url
    #le decimos al get el campo que deseamos obtener
   # project.objects.create(name = request.GET['name'] )
   
   #2da forma cSon metodo POST
   if request.method == 'GET':
       #show interface
       return render(request, "correoForm.html",{
           'form': correoForm
       })
   else:
       mail = request.POST['direccion']
       send_mail(mail)
       return redirect ('/gracias/')

@login_required   
def gracias (request):
    return render (request, 'gracias.html')

@login_required
def analisis (request):
    return render (request, 'Analisis.html')

@login_required
def tabla (request):
    return render (request, 'tabla.html')

@login_required
def variables (request):
    return render (request, 'variables.html')

@login_required
def r_salud (request):
    return render (request, 'resultado_salud.html')

@login_required
def r_horas (request):
    return render (request, 'resultado_horas.html')

@login_required
def r_inter (request):
    return render (request, 'resultado_internet.html')

@login_required
def r_borrachera (request):
    return render (request, 'resultado_borrachera.html')

@login_required
def r_resi (request):
    return render (request, 'resultado_residencia.html')

@login_required
def r_pisados (request):
    return render (request, 'resultado_pisados.html')

@login_required
def r_fisitonazo (request):
    return render (request, 'resultado_fisitonazo.html')