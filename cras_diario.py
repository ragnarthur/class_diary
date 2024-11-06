# cras_diario.py

import sys
import os

# Diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# Adiciona o diretório base ao sys.path
sys.path.insert(0, basedir)

from cras_app import create_app
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env
load_dotenv(os.path.join(basedir, '.env'))

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
