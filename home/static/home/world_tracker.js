let labels = [];
let confirmed_data = [];
let deaths_data = [];
let myChart;

// toggle tabs 
$("document").ready(() => {
    $(".tab-slider--body").hide();
    $(".tab-slider--body:first").show();
});

// don't make this arrow func cuz we can't access "this" in arrow funcs
$(".tab-slider--nav li").click(function() {
    $(".tab-slider--body").hide();
    let activeTab = $(this).attr("rel");
    $("#" + activeTab).fadeIn();
    if ($(this).attr("rel") == "tab2") {
        $('.tab-slider--tabs').addClass('slide');
        // check Confirmed radio button 
        document.getElementById("Confirmed").checked = true;

        // populate labels, confirmed_data, deaths_data from json file saved by statsApi if they are empty 
        $.getJSON("static/home/chart_data.json", (data) => {

            if (labels.length == 0) {
                for (let key in data) {
                    labels.push(key);
                    confirmed_data.push(data[key]["Confirmed"]);
                    deaths_data.push(data[key]["Deaths"]);
                }
            }
            displayChart(confirmed_data, "Confirmed Cases");
        });

    } else {
        $('.tab-slider--tabs').removeClass('slide');
    }

    $(".tab-slider--nav li").removeClass("active");
    $(this).addClass("active");
});

//setting onclick of radios
let radios = document.querySelectorAll('input[name="radio"]')
radios[0].onclick = () => {
    displayChart(confirmed_data, "Confirmed Cases");
}

radios[1].onclick = () => {
    displayChart(deaths_data, "Death Cases", "#CB0C23");
}

//displays chart
function displayChart(myData, title, color = "#F89C06") {
    //to render new chart every time
    if (myChart) {
        myChart.destroy();
    }
    let ctx = document.getElementById("myChart").getContext('2d');

    let data = {
        labels: labels,
        datasets: [{
            label: title,
            data: myData,
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
$(document).ready(() => {
    $('[data-toggle="popover"]').popover({
        placement: 'top',
        trigger: 'hover'
    });
});