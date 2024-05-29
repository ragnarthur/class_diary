import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cras_diario.settings')
django.setup()

from alunos.models import Turma, Aluno, Horario

# Criação de Turmas
turma_matutina = Turma.objects.create(nome='Turma Matutina')
turma_vespertina = Turma.objects.create(nome='Turma Vespertina')

# Criação de Horários
horarios = [
    {'dia': 'terça-feira', 'horario': '08:30-10:00', 'turma': turma_matutina},
    {'dia': 'terça-feira', 'horario': '13:30-16:00', 'turma': turma_vespertina},
    {'dia': 'quarta-feira', 'horario': '08:30-10:00', 'turma': turma_matutina},
    {'dia': 'quarta-feira', 'horario': '13:30-16:00', 'turma': turma_vespertina},
    {'dia': 'sexta-feira', 'horario': '08:30-11:00', 'turma': turma_matutina},
    {'dia': 'sexta-feira', 'horario': '13:00-17:00', 'turma': turma_vespertina},
]

for horario_info in horarios:
    Horario.objects.create(**horario_info)

# Nomes fictícios para alunos
nomes_ficticios = [
    "Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda",
    "Gabriel", "Helena", "Igor", "Juliana", "Lucas", "Mariana",
    "Nicolas", "Olivia", "Paulo", "Quintina", "Ricardo", "Sofia",
    "Tiago", "Ursula", "Vinicius", "Wagner", "Ximena", "Yasmin", "Zeca"
]

# Alocar 12 alunos por horário
for horario in Horario.objects.all():
    for nome in nomes_ficticios[:12]:
        aluno = Aluno.objects.create(nome=nome, turma=horario.turma)
        horario.alunos.add(aluno)
