# migration script to remove students with simple names

from django.db import migrations

def remove_simple_names(apps, schema_editor):
    Aluno = apps.get_model('alunos', 'Aluno')
    # Definir um critério para identificar nomes simples
    # Aqui estamos assumindo que nomes simples são aqueles sem espaços (somente o primeiro nome)
    alunos_simples = Aluno.objects.filter(nome__regex=r'^[^\s]+$')
    alunos_simples.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0005_populate_db'),
    ]

    operations = [
        migrations.RunPython(remove_simple_names),
    ]
