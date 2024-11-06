# init_db.py

import sys
import os

# Diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# Adiciona o diretório base ao sys.path
sys.path.insert(0, basedir)

from cras_app import create_app
from cras_app.extensions import db
from cras_app.models import User
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env
load_dotenv(os.path.join(basedir, '.env'))

app = create_app()

with app.app_context():
    # Verifica se o usuário admin já existe
    user = User.query.filter_by(username='admin').first()
    if not user:
        # Cria o usuário admin com a senha padrão
        user = User(username='admin')
        user.set_password('arthur123@')
        db.session.add(user)
        db.session.commit()
        print("Usuário admin criado com a senha padrão.")
    else:
        print("Usuário admin já existe.")
