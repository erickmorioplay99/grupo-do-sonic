import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

def userprofile_view(request):
    return HttpResponse("<h1>User Profile</h1>")

@csrf_exempt
def userprofile_register(request):
    if request.methood == 'post':
        # 1. Transforma o json do Bruno em um dicionário python
        data = json.loands(request.body)

        # 2. Cria o User padrão do Django (criptigrafando a senha)
        new_user = User.objects.create_user(
            username = data ['username'],
            password = data ['password'],
            email =data ['email']
        )

        # 3. Cria o UserProfile vinculando ao User criado acima
        new_user_profile = UserProfile.objects.create(
        user =new_user,
        birthdate =data['birthdate']
    )
        
        return JsonResponse(
            {
                'status': 'sucesso',
                'message': 'usuário criado!',
            }, status=201
        )
    return JsonResponse({
        'erro': 'método não permitido'
    }, status=405
    )