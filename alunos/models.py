from django.db import models

class Turma(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')

    def __str__(self):
        return self.nome

class Horario(models.Model):
    dia = models.CharField(max_length=100)
    horario = models.CharField(max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='horarios')
    alunos = models.ManyToManyField(Aluno, related_name='horarios', blank=True)

    def __str__(self):
        return f"{self.dia} ({self.horario})"

class Presenca(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField()

    def __str__(self):
        return f"{self.aluno.nome} - {'Presente' if self.presente else 'Faltou'} em {self.data}"
