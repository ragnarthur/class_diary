from django.urls import path
from .views import home, turma_list, aluno_add, horario_add, turma_add, presenca_add, sobre, professores, save_presences_matutina, save_presences_vespertina, export_presences_to_excel, desempenho_presencas, alunos_atendidos_por_mes

urlpatterns = [
    path('', home, name='home'),
    path('turmas/', turma_list, name='turma_list'),
    path('turma/<int:turma_id>/add/', aluno_add, name='aluno_add'),
    path('turma/<int:turma_id>/horario/', horario_add, name='horario_add'),
    path('turma/add/', turma_add, name='turma_add'),
    path('presenca/<int:aluno_id>/add/', presenca_add, name='presenca_add'),
    path('sobre/', sobre, name='sobre'),
    path('professores/', professores, name='professores'),
    path('save_presences_matutina/', save_presences_matutina, name='save_presences_matutina'),
    path('save_presences_vespertina/', save_presences_vespertina, name='save_presences_vespertina'),
    path('export_presences_to_excel/', export_presences_to_excel, name='export_presences_to_excel'),
    path('desempenho_presencas/', desempenho_presencas, name='desempenho_presencas'),
    path('alunos_atendidos_por_mes/', alunos_atendidos_por_mes, name='alunos_atendidos_por_mes'),
]
