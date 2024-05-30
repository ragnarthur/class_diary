from django.db import migrations, models

def add_students(apps, schema_editor):
    Aluno = apps.get_model('alunos', 'Aluno')
    Turma = apps.get_model('alunos', 'Turma')

    # Obtenha as turmas matutinas e vespertinas
    turma_matutina, _ = Turma.objects.get_or_create(nome='Matutina')
    turma_vespertina, _ = Turma.objects.get_or_create(nome='Vespertina')

    # Lista de alunos com nomes completos
    alunos = [
        ("Ana Clara Souza Silva", turma_matutina),
        ("Bruno Henrique Oliveira Costa", turma_matutina),
        ("Carla Beatriz Santos Pereira", turma_matutina),
        ("Daniel Lucas Rodrigues Lima", turma_matutina),
        ("Eduarda Gabriela Almeida Ferreira", turma_matutina),
        ("Felipe Gustavo Barbosa Rocha", turma_matutina),
        ("Gabriela Mariana Ribeiro Martins", turma_matutina),
        ("Hugo Matheus Fernandes Ribeiro", turma_matutina),
        ("Isabela Vitória Nunes Fernandes", turma_matutina),
        ("João Pedro Carvalho Pinto", turma_matutina),
        ("Lara Luiza Ramos Teixeira", turma_matutina),
        ("Mateus Leonardo Almeida Dias", turma_matutina),

        ("Nathalia Eduarda Araujo Rocha", turma_vespertina),
        ("Otávio Rafael Castro Correia", turma_vespertina),
        ("Pietra Julia Carvalho Campos", turma_vespertina),
        ("Rafael Vinicius Ribeiro Alves", turma_vespertina),
        ("Sophia Vitória Lima Barbosa", turma_vespertina),
        ("Thiago Henrique Pereira Nascimento", turma_vespertina),
        ("Vitória Beatriz Costa Figueiredo", turma_vespertina),
        ("Yasmin Letícia Martins Azevedo", turma_vespertina),
        ("Zoe Lara Ferreira Moreira", turma_vespertina),
        ("Alexandre Gabriel Rodrigues Lima", turma_vespertina),
        ("Bianca Isadora Nunes Fernandes", turma_vespertina),
        ("Caio Matheus Almeida Dias", turma_vespertina)
    ]

    # Adicione os alunos ao banco de dados
    for nome, turma in alunos:
        Aluno.objects.create(nome=nome, turma=turma)

class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_students),
    ]
