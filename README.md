
# CRAS Diário - Class Diary System

Este projeto é um sistema de diário de classe desenvolvido para gerenciar a presença dos alunos em diferentes unidades do CRAS (Centro de Referência em Assistência Social). O sistema permite que o professor ou administrador acompanhe as presenças e ausências dos alunos por data, além de visualizar estatísticas de frequência em um dashboard.

## Funcionalidades

- **Adicionar Aluno**: Cadastro de novos alunos, incluindo nome, unidade e turno.
- **Lista de Alunos**: Visualização e gestão da presença dos alunos.
- **Dashboard**: Resumo das presenças e ausências dos alunos por unidade.
- **Consulta por Data**: Permite verificar o registro de presença por datas específicas.

## Estrutura do Projeto

- **Frontend**: Desenvolvido com HTML, CSS (Bulma) e JavaScript.
- **Backend**: Flask para o gerenciamento das rotas e integração com o banco de dados.
- **Banco de Dados**: SQLite, onde são armazenados os dados dos alunos e suas presenças.

## Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/ragnarthur/class_diary.git
   cd class_diary
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # No Windows use `.venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente no arquivo `.env`.

5. Execute o aplicativo:
   ```bash
   flask run
   ```

## Uso

- Acesse o sistema através do navegador, faça login e utilize as funcionalidades disponíveis para gerenciar os alunos e visualizar o dashboard.

## Estrutura de Arquivos

- `app.py`: Arquivo principal para execução do aplicativo Flask.
- `static/`: Arquivos estáticos como CSS e JavaScript.
- `templates/`: Templates HTML.
- `.env`: Arquivo de configuração com variáveis de ambiente.
- `.gitignore`: Arquivos e diretórios ignorados no repositório.

## Contribuição

Sinta-se à vontade para contribuir com o desenvolvimento deste projeto enviando pull requests ou relatando problemas.

## Licença

Este projeto está licenciado sob a MIT License.
