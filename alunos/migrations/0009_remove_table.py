# migration script to drop the old tables

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0005_populate_db'),  # Atualize esta linha com a migração correta se necessário
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "DROP TABLE IF EXISTS alunos_alunosimples;",
                "DROP TABLE IF EXISTS alunos_alunonomecompleto;"  # Atualize o nome da tabela antiga se necessário
            ],
            reverse_sql=[
                # Opcionalmente, você pode adicionar comandos para recriar as tabelas no caso de reversão
            ],
        ),
    ]
