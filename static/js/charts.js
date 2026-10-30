document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("riskChart");

    if (!canvas || typeof riskCounts === "undefined") {
        return;
    }

    new Chart(canvas, {
        type: "doughnut",

        data: {
            labels: ["Low", "Medium", "High", "Critical"],

            datasets: [{
                data: [
                    riskCounts.Low,
                    riskCounts.Medium,
                    riskCounts.High,
                    riskCounts.Critical
                ],

                backgroundColor: [
                    "#22c55e",
                    "#eab308",
                    "#f97316",
                    "#ef4444"
                ],

                borderWidth: 0
            }]
        },

        options: {
            responsive: true,

            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });

});