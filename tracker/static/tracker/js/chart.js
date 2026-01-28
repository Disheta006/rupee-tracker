document.addEventListener('DOMContentLoaded', () => {
    const dataScript = document.getElementById('chart-data');
    if (!dataScript) return;

    let chartData;

    try {
        chartData = JSON.parse(dataScript.textContent);
    } catch (err) {
        console.error("Chart JSON parse failed", err);
        return;
    }

    const labels = chartData.labels;
    const values = chartData.values;

    if (!labels.length || !values.length) return;

    /* ===== Spending Overview ===== */
    new Chart(document.getElementById('spendingChart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                data: values,
                backgroundColor: '#14532d',
                borderRadius: 12,
                barThickness: 45
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { callback: v => `₹${v}` }
                }
            }
        }
    });

    /* ===== Category Distribution ===== */
    const total = values.reduce((a, b) => a + b, 0);
    const percentages = values.map(v => (v / total * 100).toFixed(1));

    new Chart(document.getElementById('categoryChart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                data: percentages,
                backgroundColor: '#166534',
                borderRadius: 10,
                barThickness: 18
            }]
        },
        options: {
            indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: {
                x: { max: 100, display: false }
            }
        }
    });
});