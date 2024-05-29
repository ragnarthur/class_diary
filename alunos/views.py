from django.shortcuts import render, redirect, get_object_or_404
from .models import Turma, Aluno, Horario, Presenca
from .forms import AlunoForm, HorarioForm, TurmaForm, PresencaForm
from django.utils.timezone import now, timedelta
from collections import defaultdict

def turma_list(request):
    turmas = Turma.objects.all()
    dias_da_semana = ['terça-feira', 'quarta-feira', 'sexta-feira']
    datas = {dia: (now() + timedelta(days=(i - now().weekday()) % 7)).date() for i, dia in enumerate(dias_da_semana, start=1)}

    # Separar turmas matutina e vespertina
    turmas_matutina = turmas.filter(nome__icontains='Matutina')
    turmas_vespertina = turmas.filter(nome__icontains='Vespertina')

    # Preparar presenças
    presencas_dict = defaultdict(lambda: defaultdict(lambda: None))
    for turma in turmas:
        for aluno in turma.alunos.all():
            presencas = Presenca.objects.filter(aluno=aluno, data__in=datas.values())
            for presenca in presencas:
                presencas_dict[aluno.id][presenca.data] = presenca.presente

    context = {
        'turmas_matutina': turmas_matutina,
        'turmas_vespertina': turmas_vespertina,
        'datas': datas,
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
        Presenca.objects.create(aluno=aluno, data=data, presente=presente)
        return redirect('turma_list')
    return render(request, 'presenca_form.html', {'aluno': aluno})
