document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchInput').addEventListener('keyup', function() {
        var value = this.value.toLowerCase().trim();
        var rowsMatutina = document.querySelectorAll('#performanceTableMatutina tr');
        var rowsVespertina = document.querySelectorAll('#performanceTableVespertina tr');

        rowsMatutina.forEach(function(row) {
            var turma = row.cells[0].textContent.toLowerCase();
            var aluno = row.cells[1].textContent.toLowerCase();
            
            if (turma.includes(value) || aluno.includes(value)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });

        rowsVespertina.forEach(function(row) {
            var turma = row.cells[0].textContent.toLowerCase();
            var aluno = row.cells[1].textContent.toLowerCase();
            
            if (turma.includes(value) || aluno.includes(value)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
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
