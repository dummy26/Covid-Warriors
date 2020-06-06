var labels = [];
var confirmed_data = [];
var deaths_data = [];
var myChart;

// toggle tabs 
$("document").ready(function() {
    $(".tab-slider--body").hide();
    $(".tab-slider--body:first").show();
});

$(".tab-slider--nav li").click(function() {
    $(".tab-slider--body").hide();
    var activeTab = $(this).attr("rel");
    $("#" + activeTab).fadeIn();
    if ($(this).attr("rel") == "tab2") {
        $('.tab-slider--tabs').addClass('slide');
        // check Confirmed radio button 
        document.getElementById("Confirmed").checked = true;
        // populate labels, confirmed_data, deaths_data from json file saved by statsApi if they are empty 
        $.getJSON("static/home/chart_data.json", function(data) {

            if (labels.length == 0) {
                for (var key in data) {
                    labels.push(key);
                    confirmed_data.push(data[key]["Confirmed"]);
                    deaths_data.push(data[key]["Deaths"]);
                }
            }
            displayChart(labels, confirmed_data, "Confirmed Cases");
        });

    } else {
        $('.tab-slider--tabs').removeClass('slide');
    }

    $(".tab-slider--nav li").removeClass("active");
    $(this).addClass("active");
});

//setting onclick of radios
var radios = document.querySelectorAll('input[name="radio"]')
radios[0].onclick = function() {
    displayChart(labels, confirmed_data, "Confirmed Cases");
}

radios[1].onclick = function() {
    displayChart(labels, deaths_data, "Death Cases", "#CB0C23");
}

//displays chart
function displayChart(labels, confirmed_data, title, color = "#F89C06") {
    //to render new chart every time
    if (myChart) {
        myChart.destroy();
    }
    var ctx = document.getElementById("myChart").getContext('2d');

    var data = {
        labels: labels,
        datasets: [{
            label: title,
            data: confirmed_data,
            backgroundColor: color,
            hoverBackgroundColor: "#8D8586"
        }]
    }

    myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: data,
        options: {
            title: {
                display: true,
                text: title,
                fontSize: 25,
                fontColor: 'white'
            },
            legend: {
                display: false,
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontSize: 18,
                        fontColor: 'white'
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontSize: 18,
                        fontColor: 'white'
                    }
                }]
            },
        },
    })
}

//popover on hover in map
$(document).ready(function() {
    $('[data-toggle="popover"]').popover({
        placement: 'top',
        trigger: 'hover'
    });
});