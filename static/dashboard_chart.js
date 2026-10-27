document.addEventListener("DOMContentLoaded", function () {
    if (typeof Chart === "undefined") {
        showChartError(
            "subject-average-chart-error",
            "The chart could not load. Check your internet connection and refresh the page."
        );
        showChartError(
            "gender-average-chart-error",
            "The chart could not load. Check your internet connection and refresh the page."
        );
        return;
    }

    function showChartError(errorId, message) {
        const errorElement = document.getElementById(errorId);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.hidden = false;
        }
    }

    function renderChart(canvasId, errorId, datasetLabel, colors, indexAxis = "x") {
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            showChartError(errorId, "The chart canvas could not be found.");
            return;
        }

        let chartData;
        try {
            chartData = JSON.parse(canvas.dataset.chart || "");
        } catch (error) {
            showChartError(errorId, "The chart data could not be read.");
            return;
        }

        new Chart(canvas, {
            type: "bar",
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: datasetLabel,
                    data: chartData.values,
                    backgroundColor: colors.background,
                    borderColor: colors.border,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: indexAxis,
                scales: {
                    [indexAxis === "y" ? "x" : "y"]: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    renderChart(
        "subject-average-chart",
        "subject-average-chart-error",
        "Average score",
        {
            background: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(255, 159, 64, 0.2)",
                "rgba(255, 205, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)"
            ],
            border: [
                "rgb(255, 99, 132)",
                "rgb(255, 159, 64)",
                "rgb(255, 205, 86)",
                "rgb(75, 192, 192)"
            ]
        }
    );

    renderChart(
        "gender-average-chart",
        "gender-average-chart-error",
        "Average score",
        {
            background: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)"
            ],
            border: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)"
            ]
        },
        "y"
    );
});
