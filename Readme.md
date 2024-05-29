# CRAS Diário

Este projeto é um diário de turma para os alunos do CRAS, contendo detalhes sobre nome, dia e horário das turmas, agora implementado com Django.

## Estrutura do Projeto

- `cras_diario/`: Contém o projeto Django.
  - `cras_diario/`: Configurações do projeto Django.
  - `alunos/`: Aplicativo Django para gerenciar turmas e alunos.
  - `templates/`: Templates HTML para as páginas web.
- `.gitignore`: Arquivo para especificar quais arquivos/diretórios o Git deve ignorar.
- `README.md`: Este arquivo, contendo informações sobre o projeto.
- `requirements.txt`: Arquivo para especificar dependências do projeto.
- `setup.py`: Script para configurar o pacote Python.

## Como Executar

1. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

2. Aplique as migrações do banco de dados:
    ```sh
    python manage.py migrate
    ```

3. Crie um superusuário para acessar o admin do Django:
    ```sh
    python manage.py createsuperuser
    ```

4. Execute o servidor de desenvolvimento:
    ```sh
    python manage.py runserver
    ```

5. Acesse a aplicação no navegador:
    ```
    http://127.0.0.1:8000/
    ```

## Funcionalidades

- Adicionar e remover alunos das turmas.
- Exibir detalhes das turmas.
- Interface web para facilitar a interação.
- Admin do Django para gerenciar dados.

## Admin do Django

Acesse o admin do Django para gerenciar as turmas e alunos:
