// dashboard.js - Arquivo estático puro (sem tags Django = sem erros no VSCode!)

document.addEventListener('DOMContentLoaded', function () {
    // Dados injetados pelo template via data attributes (vamos passar do HTML)
    const faixasDados = JSON.parse(document.getElementById('faixas-data').textContent);
    const generoLabels = JSON.parse(document.getElementById('genero-labels').textContent);
    const generoDados = JSON.parse(document.getElementById('genero-data').textContent);

    // Gráfico de Faixa Etária
    new Chart(document.getElementById('faixaEtariaChart'), {
        type: 'bar',
        data: {
            labels: ['60-69', '70-79', '80-89', '90+'],
            datasets: [{
                label: 'Número de Pacientes',
                data: faixasDados,
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });

    // Gráfico de Gênero
    new Chart(document.getElementById('generoChart'), {
        type: 'pie',
        data: {
            labels: generoLabels,
            datasets: [{
                data: generoDados,
                backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeead']
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'right' } }
        }
    });
});