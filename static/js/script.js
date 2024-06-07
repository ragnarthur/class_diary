document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchInput').addEventListener('keyup', function() {
        const value = this.value.toLowerCase().trim();

        function filterTable(tableId) {
            const rows = document.querySelectorAll('#' + tableId + ' tbody tr');
            rows.forEach(function(row) {
                const turma = row.querySelector('.turma').textContent.toLowerCase();
                const aluno = row.querySelector('.aluno').textContent.toLowerCase();
                if (turma.includes(value) || aluno.includes(value)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        }

        filterTable('performanceTableMatutina');
        filterTable('performanceTableVespertina');
    });
});

$(document).ready(function(){
    $('#datePicker').datepicker({
        format: 'yyyy-mm-dd',
        language: 'pt-BR',
        autoclose: true,
        todayHighlight: true
    }).on('changeDate', function(e) {
        $('#dateForm').submit();
    });
});
