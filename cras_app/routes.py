# cras_app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from cras_app.extensions import db
from .forms import LoginForm, AddStudentForm
from .models import User, Student, Attendance
from datetime import date, datetime

bp = Blueprint('main', __name__)

# Rota da página inicial
@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Início')

# Rota de login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nome de usuário ou senha incorretos', 'is-danger')
            return redirect(url_for('main.login'))

        login_user(user, remember=form.remember_me.data)
        flash('Login realizado com sucesso!', 'is-primary')

        next_page = request.args.get('next')
        if next_page and urlparse(next_page).netloc == '':
            return redirect(next_page)
        return redirect(url_for('main.index'))
        
    return render_template('login.html', form=form)

# Rota de logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'is-info')
    return redirect(url_for('main.login'))

# Rota para adicionar um novo aluno
@bp.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data.upper(),
            unit=form.unit.data,
            class_shift=form.class_shift.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Aluno adicionado com sucesso!', 'is-success')
        return redirect(url_for('main.add_student'))
    return render_template('add_student.html', title='Adicionar Aluno', form=form)

# Rota para visualizar os alunos separados por unidade e em ordem alfabética
@bp.route('/students')
@login_required
def students():
    santa_rita_students = Student.query.filter_by(unit='Santa Rita').order_by(Student.name).all()
    vila_nova_students = Student.query.filter_by(unit='Vila Nova').order_by(Student.name).all()
    celso_bueno_students = Student.query.filter_by(unit='Celso Bueno').order_by(Student.name).all()

    for student in santa_rita_students + vila_nova_students + celso_bueno_students:
        latest_attendance = Attendance.query.filter_by(student_id=student.id).order_by(Attendance.attendance_date.desc()).first()
        student.attendance_status = latest_attendance.status if latest_attendance else None

    return render_template(
        'students.html', 
        title='Lista de Alunos',
        santa_rita_students=santa_rita_students,
        vila_nova_students=vila_nova_students,
        celso_bueno_students=celso_bueno_students
    )

# Rota para atualizar o status de presença de um aluno
@bp.route('/update_attendance/<int:student_id>', methods=['POST'])
@login_required
def update_attendance(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    if 'attendance_status' in data:
        attendance = Attendance.query.filter_by(
            student_id=student.id, 
            attendance_date=date.today()
        ).first()
        if attendance:
            attendance.status = data['attendance_status']
            attendance.attendance_time = datetime.utcnow().time()
        else:
            attendance = Attendance(
                student_id=student.id, 
                status=data['attendance_status'], 
                attendance_date=date.today(),
                attendance_time=datetime.utcnow().time()
            )
            db.session.add(attendance)
        db.session.commit()
        flash('Presenças salvas com sucesso!', 'primary')
        return jsonify({'success': True, 'status': attendance.status}), 200
    return jsonify({'success': False}), 400

# Rota para salvar presenças
@bp.route('/save_attendance', methods=['POST'])
@login_required
def save_attendance():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Nenhum dado recebido'}), 400

    try:
        for student_id, status in data.items():
            student = Student.query.get(student_id)
            if not student:
                continue

            attendance = Attendance.query.filter_by(
                student_id=student.id, 
                attendance_date=date.today()
            ).first()
            if attendance:
                attendance.status = status
                attendance.attendance_time = datetime.utcnow().time()
            else:
                attendance = Attendance(
                    student_id=student.id,
                    status=status,
                    attendance_date=date.today(),
                    attendance_time=datetime.utcnow().time()
                )
                db.session.add(attendance)

        db.session.commit()
        return jsonify({'success': True}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# Rota para excluir um aluno
@bp.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    # Exclua todas as presenças associadas ao aluno antes de excluir o aluno
    Attendance.query.filter_by(student_id=student.id).delete()
    
    db.session.delete(student)
    db.session.commit()
    
    flash('Aluno excluído com sucesso!', 'is-danger')
    return redirect(url_for('main.students'))

# Rota para visualizar presenças acumuladas até o momento
@bp.route('/attendance_summary')
@login_required
def attendance_summary():
    all_attendances = Attendance.query.order_by(Attendance.attendance_date.desc()).all()
    summary_by_unit = {
        'Santa Rita': {},
        'Vila Nova': {},
        'Celso Bueno': {}
    }
    for attendance in all_attendances:
        student = attendance.student
        date_key = attendance.attendance_date.strftime('%Y-%m-%d')
        if date_key not in summary_by_unit[student.unit]:
            summary_by_unit[student.unit][date_key] = []
        summary_by_unit[student.unit][date_key].append({
            'name': student.name,
            'class_shift': student.class_shift,
            'attendance_date': attendance.attendance_date,
            'status': attendance.status
        })

    return render_template(
        'attendance_summary.html',
        title='Resumo de Presenças',
        summary_by_unit=summary_by_unit
    )

# Rota para consultar presença por data
@bp.route('/attendance/<string:attendance_date>')
@login_required
def attendance_by_date(attendance_date):
    attendance_date = date.fromisoformat(attendance_date)
    attendance_records = Attendance.query.filter_by(attendance_date=attendance_date).all()
    students_by_unit = {
        'Santa Rita': [],
        'Vila Nova': [],
        'Celso Bueno': []
    }
    for record in attendance_records:
        student = record.student
        students_by_unit[student.unit].append({
            'name': student.name,
            'class_shift': student.class_shift,
            'attendance_status': record.status,
            'attendance_time': record.attendance_time.strftime('%H:%M')
        })
    
    return render_template(
        'attendance_by_date.html', 
        title=f'Diário de {attendance_date}', 
        students_by_unit=students_by_unit, 
        attendance_date=attendance_date
    )

# Rota para o dashboard
@bp.route('/dashboard')
@login_required
def dashboard():
    dashboard_data = {
        "Santa Rita": {"total": 0, "presentes": 0, "ausentes": 0},
        "Vila Nova": {"total": 0, "presentes": 0, "ausentes": 0},
        "Celso Bueno": {"total": 0, "presentes": 0, "ausentes": 0}
    }

    for unit in dashboard_data.keys():
        students = Student.query.filter_by(unit=unit).all()
        dashboard_data[unit]["total"] = len(students)
        for student in students:
            today_attendance = Attendance.query.filter_by(
                student_id=student.id,
                attendance_date=date.today()
            ).first()
            if today_attendance:
                if today_attendance.status == "Presente":
                    dashboard_data[unit]["presentes"] += 1
                elif today_attendance.status == "Ausente":
                    dashboard_data[unit]["ausentes"] += 1

    return render_template('dashboard.html', title='Dashboard', dashboard_data=dashboard_data)
