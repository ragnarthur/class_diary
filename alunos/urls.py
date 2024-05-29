from django.urls import path
from .views import turma_list, aluno_add, horario_add, turma_add, presenca_add

urlpatterns = [
    path('', turma_list, name='turma_list'),
    path('turma/<int:turma_id>/add/', aluno_add, name='aluno_add'),
    path('turma/<int:turma_id>/horario/', horario_add, name='horario_add'),
    path('turma/add/', turma_add, name='turma_add'),
    path('presenca/<int:aluno_id>/add/', presenca_add, name='presenca_add'),
]
