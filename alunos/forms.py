from django import forms
from .models import Aluno, Horario, Turma, Presenca

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome']

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['dia', 'horario', 'alunos']

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome']

class PresencaForm(forms.ModelForm):
    class Meta:
        model = Presenca
        fields = ['aluno', 'data', 'presente']
