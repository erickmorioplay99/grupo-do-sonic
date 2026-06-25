from django.urls import path
from . import views

urlpatterns = [
    # Altere ou adicione uma linha assim:
    path('view/', views.userprofile_view, name='userprofile_view'),
    
    # ... suas outras rotas
]