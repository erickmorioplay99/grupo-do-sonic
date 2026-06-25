import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile

# superuser - admin - t3st3s3c

# Create your views here.
def home_view(request):
    return render(request, 'home.html')

@csrf_exempt
def userprofile_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            if user is not None:
                login(request, user)  # <--- ESSENCIAL: Isso cria a sessão e prepara o cookie
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def userprofile_view(request):
    """
    POST /userprofile/view/
    Retorna os dados do usuário autenticado. Requer sessão ativa.
    """
    if request.method == 'POST':
        usuario = request.user
        
        # Busca o perfil vinculado ao usuário logado
        profile = UserProfile.objects.filter(user=usuario).first()
        
        usuario_data = {
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'birthdate': profile.birthdate.isoformat() if profile and profile.birthdate else None,
        }
        return JsonResponse({'success': True, 'usuario': usuario_data})

    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt
def userprofile_list(request):
    """
    POST /userprofile/list/
    Retorna a lista de perfis de usuários. Requer usuário staff autenticado.
    """
    if request.method == 'POST':
        usuario = request.user
        
        # Valida se o usuário autenticado possui permissão de staff
        if not usuario.is_staff:
            return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
            
        # Busca todos os perfis cadastrados no sistema
        perfis = UserProfile.objects.all()
        usuarios_data = []

        for perfil in perfis:
            usuarios_data.append({
                'id': perfil.id,
                'username': perfil.user.username,
                'email': perfil.user.email,
                'birthdate': perfil.birthdate.isoformat() if perfil.birthdate else None
            })
            
        return JsonResponse({'success': True, 'usuarios': usuarios_data})

    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt
def userprofile_register(request):
    if request.method == 'POST':
        # 1. Transforma o JSON do Bruno em um dicionário python
        data = json.loads(request.body)

        # 2. Cria o User padrão do Django (criptografando a senha)
        new_user = User.objects.create_user(
            username = data['username'],
            password = data['password'],
            email = data['email']
        )

        # 3. Cria o UserProfile vinculando ao User criado acima
        new_user_profile = UserProfile.objects.create(
            user = new_user,
            birthdate = data['birthdate']
        )

        return JsonResponse(
            {
                'status': 'Sucesso',
                'message': 'Usuário criado!',
            }, status=201
        )
    return JsonResponse({'erro': 'Método não permitido'}, status=405)
