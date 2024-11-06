from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired

# Formulário de login
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

# Formulário para adicionar aluno
class AddStudentForm(FlaskForm):
    name = StringField('Nome do Aluno', validators=[DataRequired()])
    unit = SelectField('Unidade', choices=[
        ('Santa Rita', 'Santa Rita'),
        ('Vila Nova', 'Vila Nova'),
        ('Celso Bueno', 'Celso Bueno')
    ], validators=[DataRequired()])
    class_shift = SelectField('Turma', choices=[
        ('Matutina', 'Matutina (8:30 às 10:00)'),
        ('Vespertina', 'Vespertina (13:30 às 16:00)'),
        ('Instrumento_Sexta_Matutina', 'Instrumento (Sexta-feira 8:00 às 11:00)'),
        ('Instrumento_Sexta_Vespertina', 'Instrumento (Sexta-feira 13:00 às 17:00)')
    ], validators=[DataRequired()])
    submit = SubmitField('Adicionar Aluno')
