document.addEventListener('DOMContentLoaded', function() {
    const attendanceSummary = { present: 0, absent: 0 };

    // Função para atualizar a presença no servidor
    function updateAttendanceOnServer(studentId, status) {
        fetch(`/update_attendance/${studentId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ attendance_status: status })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Status de presença atualizado com sucesso.');
            } else {
                console.log('Erro ao atualizar o status de presença.');
            }
        })
        .catch(error => console.error('Erro:', error));
    }

    // Botões de presença e ausência
    document.querySelectorAll('.mark-present').forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const studentId = row.getAttribute('data-student-id');
            row.classList.add('present');
            row.classList.remove('absent');
            row.querySelector('.attendance-status').textContent = 'Presente';
            attendanceSummary.present += 1;
            if (attendanceSummary.absent > 0) attendanceSummary.absent -= 1;
            updateAttendanceOnServer(studentId, 'Presente');
            updateAttendanceSummary();
        });
    });

    document.querySelectorAll('.mark-absent').forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const studentId = row.getAttribute('data-student-id');
            row.classList.add('absent');
            row.classList.remove('present');
            row.querySelector('.attendance-status').textContent = 'Ausente';
            attendanceSummary.absent += 1;
            if (attendanceSummary.present > 0) attendanceSummary.present -= 1;
            updateAttendanceOnServer(studentId, 'Ausente');
            updateAttendanceSummary();
        });
    });

    // Atualiza o resumo de frequência
    function updateAttendanceSummary() {
        const summaryDiv = document.getElementById('attendance-summary');
        summaryDiv.innerHTML = `
            <p>Presentes: ${attendanceSummary.present}</p>
            <p>Ausentes: ${attendanceSummary.absent}</p>
        `;
    }

    // Função para alternância de abas
    const tabs = document.querySelectorAll('.tabs ul li');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('is-active'));
            tabPanes.forEach(pane => pane.classList.remove('is-active'));
            tab.classList.add('is-active');
            document.getElementById(tab.dataset.tab).classList.add('is-active');
        });
    });

    // Função para atualização de data e hora
    function updateDateTime() {
        const now = new Date();
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric', 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit' 
        };
        const dateTimeElement = document.getElementById('current-datetime');
        if (dateTimeElement) {
            dateTimeElement.textContent = now.toLocaleDateString('pt-BR', options);
        }
    }

    setInterval(updateDateTime, 1000);
    updateDateTime();

    // Verificação e atualização do diário por data
    const viewAttendanceButton = document.getElementById('view-attendance');
    const attendanceDateInput = document.getElementById('attendance-date');

    viewAttendanceButton.addEventListener('click', function () {
        const selectedDate = attendanceDateInput.value;
        if (selectedDate) {
            window.location.href = `/students?attendance_date=${selectedDate}`;
        } else {
            alert("Por favor, selecione uma data para consulta.");
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Função para atualizar o resumo do dashboard em tempo real (por AJAX)
    function updateDashboard() {
        fetch('/api/dashboard_data')
            .then(response => response.json())
            .then(data => {
                document.getElementById('santa-rita-total').textContent = data.santa_rita.total;
                document.getElementById('santa-rita-presentes').textContent = data.santa_rita.presentes;
                document.getElementById('santa-rita-ausentes').textContent = data.santa_rita.ausentes;
                // Repita para as outras unidades, se necessário
            })
            .catch(error => console.error('Erro ao atualizar o dashboard:', error));
    }
    
    // Atualiza o dashboard a cada 10 segundos
    setInterval(updateDashboard, 10000);
    updateDashboard(); // Chamada inicial

    // Navegação do dashboard para consultas por data
    const viewAttendanceButton = document.getElementById('view-attendance');
    const attendanceDateInput = document.getElementById('attendance-date');

    viewAttendanceButton.addEventListener('click', function () {
        const selectedDate = attendanceDateInput.value;
        if (selectedDate) {
            window.location.href = `/students?attendance_date=${selectedDate}`;
        } else {
            alert("Por favor, selecione uma data para consulta.");
        }
    });
});
