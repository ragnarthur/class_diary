from django.shortcuts import render, redirect, get_object_or_404
from .models import Turma, Aluno, Horario, Presenca
from .forms import AlunoForm, HorarioForm, TurmaForm, PresencaForm
from django.utils.timezone import now, localtime
from collections import defaultdict
from datetime import datetime, timedelta
from babel.dates import format_date
import pandas as pd
from django.http import HttpResponse
import calendar


def home(request):
    return render(request, 'home.html')

def turma_list(request):
    data_atual = now().date()
    if 'dia' in request.GET:
        try:
            data_atual = datetime.strptime(request.GET['dia'], '%Y-%m-%d').date()
        except ValueError:
            data_atual = now().date()
    else:
        data_atual = now().date()

    nome_dia = format_date(data_atual, 'EEEE', locale='pt_BR')
    data_formatada = format_date(data_atual, "d 'de' MMMM 'de' yyyy", locale='pt_BR')

    turmas = Turma.objects.all().order_by('nome')

    turmas_matutina = turmas.filter(nome__icontains='Matutina')
    turmas_vespertina = turmas.filter(nome__icontains='Vespertina')

    presencas_dict = defaultdict(lambda: None)
    for turma in turmas:
        for aluno in turma.alunos.all().order_by('nome'):
            presenca = Presenca.objects.filter(aluno=aluno, data=data_atual).first()
            if presenca:
                presencas_dict[aluno.id] = presenca.presente

    context = {
        'turmas_matutina': turmas_matutina,
        'turmas_vespertina': turmas_vespertina,
        'data_atual': data_atual,
        'presencas_dict': presencas_dict,
        'nome_dia': nome_dia,
        'data_formatada': data_formatada,
        'now': now
    }
    return render(request, 'turma_list.html', context)

def save_presences_matutina(request):
    if request.method == 'POST':
        data_atual = now().date()
        turmas_matutina = Turma.objects.filter(nome__icontains='Matutina')
        for turma in turmas_matutina:
            for aluno in turma.alunos.all():
                presente = request.POST.get(f'presenca_{aluno.id}') == 'on'
                Presenca.objects.update_or_create(
                    aluno=aluno, data=data_atual,
                    defaults={'presente': presente}
                )
        return redirect('turma_list')

def save_presences_vespertina(request):
    if request.method == 'POST':
        data_atual = now().date()
        turmas_vespertina = Turma.objects.filter(nome__icontains='Vespertina')
        for turma in turmas_vespertina:
            for aluno in turma.alunos.all():
                presente = request.POST.get(f'presenca_{aluno.id}') == 'on'
                Presenca.objects.update_or_create(
                    aluno=aluno, data=data_atual,
                    defaults={'presente': presente}
                )
        return redirect('turma_list')

def export_presences_to_excel(request):
    # Determinar o intervalo de datas para exportação
    export_type = request.GET.get('type', 'manual')
    year = request.GET.get('year', localtime(now()).year)
    month = request.GET.get('month', localtime(now()).month)
    
    if export_type == 'monthly':
        start_date = datetime(int(year), int(month), 1).date()
        end_date = datetime(int(year), int(month), calendar.monthrange(int(year), int(month))[1]).date()
    else:
        start_date = request.GET.get('start_date', localtime(now()).date())
        end_date = request.GET.get('end_date', localtime(now()).date())

    turmas = Turma.objects.all().order_by('nome')
    data = []

    for turma in turmas:
        for aluno in turma.alunos.all().order_by('nome'):
            presencas = Presenca.objects.filter(aluno=aluno, data__range=[start_date, end_date]).order_by('data')
            for presenca in presencas:
                data.append([
                    turma.nome,
                    aluno.nome,
                    presenca.data,
                    'Presente' if presenca.presente else 'Falta'
                ])

    df = pd.DataFrame(data, columns=['Turma', 'Aluno', 'Data', 'Presença'])
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=presencas_{year}_{month}.xlsx'
    df.to_excel(response, index=False)

    return response

def desempenho_presencas(request):
    turmas = Turma.objects.all().order_by('nome')
    desempenho = []

    for turma in turmas:
        alunos = turma.alunos.all().order_by('nome')
        for aluno in alunos:
            total_presencas = Presenca.objects.filter(aluno=aluno, presente=True).count()
            total_faltas = Presenca.objects.filter(aluno=aluno, presente=False).count()
            desempenho.append({
                'turma': turma.nome,
                'aluno': aluno.nome,
                'total_presencas': total_presencas,
                'total_faltas': total_faltas
            })

    context = {
        'desempenho': desempenho
    }
    return render(request, 'desempenho_presencas.html', context)

def alunos_atendidos_por_mes(request):
    current_time = localtime(now())
    start_date = current_time.replace(day=1)
    end_date = current_time.replace(day=calendar.monthrange(current_time.year, current_time.month)[1])

    turmas = Turma.objects.all().order_by('nome')
    atendidos_matutina = Presenca.objects.filter(data__range=[start_date, end_date], aluno__turma__nome__icontains='Matutina', presente=True).values('aluno').distinct().count()
    atendidos_vespertina = Presenca.objects.filter(data__range=[start_date, end_date], aluno__turma__nome__icontains='Vespertina', presente=True).values('aluno').distinct().count()

    context = {
        'atendidos_matutina': atendidos_matutina,
        'atendidos_vespertina': atendidos_vespertina,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'alunos_atendidos_por_mes.html', context)


def aluno_add(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.turma = turma
            aluno.save()
            return redirect('turma_list')
    else:
        form = AlunoForm()
    return render(request, 'aluno_form.html', {'form': form, 'turma': turma})

def horario_add(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.turma = turma
            horario.save()
            form.save_m2m()
            return redirect('turma_list')
    else:
        form = HorarioForm()
    return render(request, 'horario_form.html', {'form': form, 'turma': turma})

def turma_add(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turma_list')
    else:
        form = TurmaForm()
    return render(request, 'turma_form.html', {'form': form})

def presenca_add(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    if request.method == 'POST':
        data = request.POST.get('data')
        presente = request.POST.get('presente') == 'on'
        Presenca.objects.update_or_create(
            aluno=aluno, data=data,
            defaults={'presente': presente}
        )
        return redirect('turma_list')
    return render(request, 'presenca_form.html', {'aluno': aluno})

def sobre(request):
    return render(request, 'sobre.html')

def professores(request):
    return render(request, 'professores.html')
