document.addEventListener('DOMContentLoaded', function() {
    // Função para garantir que o input de nome seja sempre em maiúsculas
    const nameInput = document.querySelector('.name-input');
    if (nameInput) {
        nameInput.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    }

    // Função para atualizar a presença no servidor
    function updateAttendanceOnServer(studentId, status) {
        fetch(`/update_attendance/${studentId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ attendance_status: status })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro na solicitação: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log('Status de presença atualizado com sucesso.');
            } else {
                console.log('Erro ao atualizar o status de presença.');
            }
        })
        .catch(error => console.error('Erro na atualização de presença:', error));
    }

    // Botões de presença e ausência
    const attendanceData = {};

    document.querySelectorAll('.mark-present').forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const studentId = row.getAttribute('data-student-id');
            if (!studentId) {
                console.error('ID do aluno não encontrado para a linha selecionada.');
                return;
            }
            row.classList.add('present');
            row.classList.remove('absent');
            row.querySelector('.attendance-status').textContent = 'Presente';
            attendanceData[studentId] = 'Presente';
            updateAttendanceOnServer(studentId, 'Presente');
        });
    });

    document.querySelectorAll('.mark-absent').forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const studentId = row.getAttribute('data-student-id');
            if (!studentId) {
                console.error('ID do aluno não encontrado para a linha selecionada.');
                return;
            }
            row.classList.add('absent');
            row.classList.remove('present');
            row.querySelector('.attendance-status').textContent = 'Ausente';
            attendanceData[studentId] = 'Ausente';
            updateAttendanceOnServer(studentId, 'Ausente');
        });
    });

    // Função para salvar presenças ao clicar no botão
    const saveButton = document.getElementById('save-attendance');
    if (saveButton) {
        saveButton.addEventListener('click', function() {
            fetch('/save_attendance', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(attendanceData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro na solicitação: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const successMessage = document.getElementById('success-message');
                    if (successMessage) {
                        successMessage.classList.remove('is-hidden');
                        setTimeout(() => {
                            successMessage.classList.add('is-hidden');
                            // Redireciona para a página inicial após 3 segundos
                            window.location.href = '/';
                        }, 3000);
                    } else {
                        // Redireciona imediatamente se a mensagem de sucesso não for encontrada
                        window.location.href = '/';
                    }
                } else {
                    alert('Erro ao salvar as presenças.');
                }
            })
            .catch(error => {
                console.error('Erro ao salvar presenças:', error);
                alert('Erro ao salvar as presenças.');
            });
        });
    }

    // Função para alternância de abas
    const tabs = document.querySelectorAll('.tabs ul li');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('is-active'));
            tabPanes.forEach(pane => pane.classList.remove('is-active'));
            tab.classList.add('is-active');
            const paneId = tab.dataset.tab;
            const activePane = document.getElementById(paneId);
            if (activePane) {
                activePane.classList.add('is-active');
            } else {
                console.warn(`Pane com ID "${paneId}" não encontrado.`);
            }
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
});
