# CRAS Diary

This project is a class diary for CRAS (Centro de Referência da Assistência Social) students, detailing the names, days, and times of the classes, now implemented with Django.

## Project Structure

- `cras_diario/`: Contains the Django project.
  - `cras_diario/`: Django project settings.
  - `alunos/`: Django app for managing classes and students.
  - `templates/`: HTML templates for web pages.
- `.gitignore`: Specifies which files/directories Git should ignore.
- `README.md`: This file, containing information about the project.
- `requirements.txt`: File specifying the project dependencies.
- `setup.py`: Script for setting up the Python package.

## How to Run

1. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Apply the database migrations:
    ```sh
    python manage.py migrate
    ```

3. Create a superuser to access the Django admin:
    ```sh
    python manage.py createsuperuser
    ```

4. Run the development server:
    ```sh
    python manage.py runserver
    ```

5. Access the application in your browser:
    ```
    http://127.0.0.1:8000/
    ```

## Features

- Add and remove students from classes.
- Display class details.
- Web interface for easy interaction.
- Django admin to manage data.

## Django Admin

Access the Django admin to manage classes and students.
