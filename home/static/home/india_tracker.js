let labels = [];
let confirmed_data = [];
let deaths_data = [];
let myChart;

$.getJSON("static/home/india_pie_data.json", (data) => {
    for (let key in data) {
        labels.push(key);
        confirmed_data.push(data[key]["Confirmed"]);
        deaths_data.push(data[key]["Deaths"]);
    }
    displayChart("confirmed_pie", confirmed_data, "Confirmed Cases", true);
    displayChart("deaths_pie", deaths_data, "Death Cases");

})

//displays chart
function displayChart(id, myData, title, legend = false) {
    let ctx = document.getElementById(id).getContext('2d');


    let data = {
        labels: labels,
        datasets: [{
            label: title,
            data: myData,
            backgroundColor: [
                '#f44336', '#795548', '#4CAF50', '#03A9F4', '#9C27B0', '#FFEB3B', '#E91E63', '#3F51B5', '#64FFDA', '#FF9800', '#212121'
            ],
        }]
    }

    myChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            title: {
                display: true,
                text: title,
                fontSize: 20,
                fontColor: 'white',
            },
            legend: {
                onClick: (e) => e.stopPropagation(),
                display: legend,
                position: 'right',
                labels: {
                    fontSize: 15,
                    usePointStyle: true
                }
            },
        },
    })
}