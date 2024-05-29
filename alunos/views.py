from django.shortcuts import render, redirect, get_object_or_404
from .models import Turma, Aluno, Horario, Presenca
from .forms import AlunoForm, HorarioForm, TurmaForm, PresencaForm
from django.utils.timezone import now, timedelta
from collections import defaultdict
from datetime import datetime

def turma_list(request):
    data_atual = now().date()
    if 'dia' in request.GET:
        data_atual = datetime.strptime(request.GET['dia'], '%Y-%m-%d').date()
    else:
        data_atual = now().date()

    data_anterior = data_atual - timedelta(days=1)
    data_posterior = data_atual + timedelta(days=1)

    turmas = Turma.objects.all()

    # Separar turmas matutina e vespertina
    turmas_matutina = turmas.filter(nome__icontains='Matutina')
    turmas_vespertina = turmas.filter(nome__icontains='Vespertina')

    # Preparar presenças
    presencas_dict = defaultdict(lambda: None)
    for turma in turmas:
        for aluno in turma.alunos.all():
            presenca = Presenca.objects.filter(aluno=aluno, data=data_atual).first()
            if presenca:
                presencas_dict[aluno.id] = presenca.presente

    context = {
        'turmas_matutina': turmas_matutina,
        'turmas_vespertina': turmas_vespertina,
        'data_atual': data_atual,
        'data_anterior': data_anterior,
        'data_posterior': data_posterior,
        'presencas_dict': presencas_dict
    }
    return render(request, 'turma_list.html', context)

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
        presenca, created = Presenca.objects.update_or_create(
            aluno=aluno, data=data,
            defaults={'presente': presente}
        )
        return redirect('turma_list')
    return render(request, 'presenca_form.html', {'aluno': aluno})
