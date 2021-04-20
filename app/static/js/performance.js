var ctx = document.getElementById('chart').getContext('2d');

function getBoxWidth(labelOpts, fontSize) {
    return labelOpts.usePointStyle ?
        fontSize * Math.SQRT2 :
        labelOpts.boxWidth;
};

// Code to increase size between legend and graph
Chart.NewLegend = Chart.Legend.extend({
    afterFit: function () {
        this.height = this.height + 20;
    },
});

function createNewLegendAndAttach(chartInstance, legendOpts) {
    var legend = new Chart.NewLegend({
        ctx: chartInstance.chart.ctx,
        options: legendOpts,
        chart: chartInstance
    });

    if (chartInstance.legend) {
        Chart.layoutService.removeBox(chartInstance, chartInstance.legend);
        delete chartInstance.newLegend;
    }

    chartInstance.newLegend = legend;
    Chart.layoutService.addBox(chartInstance, legend);
}

// Register the legend plugin
Chart.plugins.register({
    beforeInit: function (chartInstance) {
        var legendOpts = chartInstance.options.legend;

        if (legendOpts) {
            createNewLegendAndAttach(chartInstance, legendOpts);
        }
    },
    beforeUpdate: function (chartInstance) {
        var legendOpts = chartInstance.options.legend;

        if (legendOpts) {
            legendOpts = Chart.helpers.configMerge(Chart.defaults.global.legend, legendOpts);

            if (chartInstance.newLegend) {
                chartInstance.newLegend.options = legendOpts;
            } else {
                createNewLegendAndAttach(chartInstance, legendOpts);
            }
        } else {
            Chart.layoutService.removeBox(chartInstance, chartInstance.newLegend);
            delete chartInstance.newLegend;
        }
    },
    afterEvent: function (chartInstance, e) {
        var legend = chartInstance.newLegend;
        if (legend) {
            legend.handleEvent(e);
        }
    }
});
// End of code to increase size between legend and graph

// var colors = [
//     { "name": "Charcoal", "hex": "264653", "rgb": [38, 70, 83], "cmyk": [54, 16, 0, 67], "hsb": [197, 54, 33], "hsl": [197, 37, 24], "lab": [28, -8, -11] },
//     { "name": "Persian Green", "hex": "2a9d8f", "rgb": [42, 157, 143], "cmyk": [73, 0, 9, 38], "hsb": [173, 73, 62], "hsl": [173, 58, 39], "lab": [59, -35, -2] },
//     { "name": "Orange Yellow Crayola", "hex": "e9c46a", "rgb": [233, 196, 106], "cmyk": [0, 16, 55, 9], "hsb": [43, 55, 91], "hsl": [43, 74, 66], "lab": [81, 2, 50] },
//     { "name": "Sandy Brown", "hex": "f4a261", "rgb": [244, 162, 97], "cmyk": [0, 34, 60, 4], "hsb": [27, 60, 96], "hsl": [27, 87, 67], "lab": [74, 24, 46] },
//     { "name": "Burnt Sienna", "hex": "e76f51", "rgb": [231, 111, 81], "cmyk": [0, 52, 65, 9], "hsb": [12, 65, 91], "hsl": [12, 76, 61], "lab": [61, 44, 38] }
// ]
// TODO: Full when hovering
var colors = [
    "rgba(38, 70, 83, 0.6)",
    "rgba(42, 157, 143, 0.6)",
    "rgba(233, 196, 106, 0.6)",
    "rgba(244, 162, 97, 0.6)",
    "rgba(231, 111, 81, 0.6)",
]

Chart.defaults.global.pointHitDetectionRadius = 1;

var customTooltips = function (tooltip) {
    // Tooltip Element
    var tooltipEl = document.getElementById('chartjs-tooltip');

    if (!tooltipEl) {
        tooltipEl = document.createElement('div');
        tooltipEl.id = 'chartjs-tooltip';
        tooltipEl.innerHTML = '<table></table>';
        this._chart.canvas.parentNode.appendChild(tooltipEl);
    }

    // Hide if no tooltip
    if (tooltip.opacity === 0) {
        tooltipEl.style.opacity = 0;
        return;
    }

    // Set caret Position
    tooltipEl.classList.remove('above', 'below', 'no-transform');
    if (tooltip.yAlign) {
        tooltipEl.classList.add(tooltip.yAlign);
    } else {
        tooltipEl.classList.add('no-transform');
    }

    function getBody(bodyItem) {
        return bodyItem.lines;
    }

    // Set Text
    if (tooltip.body) {
        var titleLines = tooltip.title || [];
        var bodyLines = tooltip.body.map(getBody);

        var innerHtml = '<thead>';

        titleLines.forEach(function (title) {
            innerHtml += '<tr><th>' + title + '</th><th>Accuracy</th></tr>';
        });
        innerHtml += '</thead><tbody>';

        bodyLines.forEach(function (body, i) {
            var colors = tooltip.labelColors[i];
            var style = 'background:' + colors.backgroundColor;
            style += '; border-color:' + colors.borderColor;
            style += '; border-width: 2px';
            var span = '<span class="chartjs-tooltip-key" style="' + style + '"></span>';
            var split_body = body[0].split(":");
            var from_type = split_body[0];
            var accuracy = parseFloat(split_body[1]).toFixed(2) + '%';
            innerHtml += '<tr><td>' + span + from_type + '</td><td style="text-align:right">&nbsp;' + accuracy + '</td></tr>';
        });
        innerHtml += '</tbody>';

        var tableRoot = tooltipEl.querySelector('table');
        tableRoot.innerHTML = innerHtml;
    }

    var positionY = this._chart.canvas.offsetTop;
    var positionX = this._chart.canvas.offsetLeft;

    var offset = tooltip.caretX;
    if (offset < tooltip.width)
        offset = tooltip.width;
    else if (tooltip.caretX > this._chart.width - tooltip.width)
        offset = this._chart.width - tooltip.width;

    // Display, position, and set styles for font
    tooltipEl.style.opacity = 1;
    tooltipEl.style.left = positionX + offset + 'px';
    tooltipEl.style.top = positionY + tooltip.caretY + 'px';
    tooltipEl.style.fontFamily = tooltip._bodyFontFamily;
    tooltipEl.style.fontSize = tooltip.bodyFontSize + 'px';
    tooltipEl.style.fontStyle = tooltip._bodyFontStyle;
    tooltipEl.style.padding = tooltip.yPadding + 'px ' + tooltip.xPadding + 'px';
};

var options = {
    layout: {
        padding: {
            // top: 20
            top: 10
        }
    },

    tooltips: {
        enabled: false,
        mode: 'index',
        position: 'nearest',
        custom: customTooltips
    },

    scales: {
        yAxes: [{
            ticks: {
                min: 90,
                max: 100,
            }
        }],
    },

    plugins: {
        datalabels: {
            // color: 'white',
            anchor: 'end',
            align: 'top',
            clamp: true, // Doesn't keep labels within graph
            formatter: function (value, context) {
                return value.toFixed(2) + '%';
            },
        },
        zoom: {
            pan: {
                enabled: true,
                mode: 'y',
                rangeMin: {
                    y: 0,
                },
                rangeMax: {
                    y: 100,
                },
            },
            zoom: {
                enabled: true,
                mode: 'y',
                rangeMin: {
                    y: 0,
                },
                rangeMax: {
                    y: 100,
                },
            }
        }
    },
    maintainAspectRatio: false,
    responsive: true,
};

/*var data = {
    labels: ['Inflex', 'LemmInflect', 'Pattern', 'PyInflect'],
    datasets: [
        {
            label: "From Past",
            data: [98.995, 95.724, 93.153, 1.010],
            backgroundColor: colors[0],
            borderWidth: 1,
        },
        {
            label: "From Pres Part",
            data: [2.7956, 96.246, 93.135, 0.006],
            backgroundColor: colors[1],
            borderWidth: 1,
        },
        {
            label: "From Singular",
            data: [97.055, 95.530, 92.604, 0.012],
            backgroundColor: colors[2],
            borderWidth: 1
        },
        {
            label: "From Plural",
            data: [96.244, 94.583, 91.737, 99.886],
            backgroundColor: colors[3],
            borderWidth: 1
        },
        {
            label: "From Past Part",
            data: [98.338, 95.367, 92.895, 1.059],
            backgroundColor: colors[4],
            borderWidth: 1
        },
    ]
};
*/

$(document).ready(function () {
    var myChart = new Chart(ctx);

    // var myChart = new Chart(ctx, {
    //     // Data is "to past"
    //     type: 'bar',
    //     data: data,
    //     options: options
    // });
    // Get array of used modules
    // const modules = JSON.parse($("#modules").text().replace(/'/g, '"'));

    // Set width for module column in table
    // var character_count = modules.map(x => x.length).reduce((accum, current_val) => Math.max(accum, current_val), $("#known_correct_module").text().length);
    // $("#module_column").css("width", `${character_count * 10}px`);

    // sending a connect request to the server.
    var socket = io.connect('http://localhost:5000');

    var wordform_to_human_readable = {
        "sing": "Singular",
        "plur": "Plural",
        "past": "Past",
        "pres_part": "Present Participle",
        "past_part": "Past Participle",
        "comp": "Comparative",
        "super": "Superlative",
    }

    var pos_to_human_readable_plural = {
        "n": "Nouns",
        "v": "Verbs",
        "a": "Adjectives",
    }

    // Emit the request for which modules should be shown
    function emit_performance() {
        socket.emit("input_performance", {
            pos: $("#pos").val(),
            wordform: $("#wordform").val(),
            source: $("#data_source").val()
        });
    }

    // Disable Past, Past Participle and Present Participle if a POS other than Verb is selected
    function toggle_wordform_disabled(pos) {
        const all_wordforms = ["sing", "plur", "past", "past_part", "pres_part", "comp", "super"];
        const wordforms = {
            "v": ["sing", "plur", "past", "past_part", "pres_part"],
            "n": ["sing", "plur"],
            "a": ["comp", "super"],
        };
        all_wordforms.forEach(word_form => {
            if (wordforms[pos].includes(word_form)) {
                $(`#wordform option[value='${word_form}']`).prop('disabled', false);
            }
            else {
                $(`#wordform option[value='${word_form}']`).prop('disabled', true);
            }
        });
        // If one of the wordforms that will be disabled has been selected, reset to the first legal option
        var wordform_selector = $('#wordform')[0];
        if (!wordforms[pos].includes(wordform_selector.value)) {
            wordform_selector.value = wordforms[pos][0];
        }
    }

    // Optionally disable Adjective if source is CELEX collocations
    function toggle_pos_disabled(source) {
        if (source == "celex_collocation") {
            $(`#pos option[value=a]`).prop('disabled', true);
            // If one of the wordforms that will be disabled has been selected, reset to the first legal option
            var pos_selector = $('#pos')[0];
            if (pos_selector.value == "a") {
                pos_selector.value = "v";
                toggle_wordform_disabled("v");
            }
        } else {
            $(`#pos option[value=a]`).prop('disabled', false);
        }
    }

    // Straight away find which modules can be used
    emit_performance();

    // Update which Wordform options are allowed, given the current POS,
    // also find out which modules should be shown given the current POS and Wordform
    $('#pos').change(function () {
        toggle_wordform_disabled(this.value);

        // Emit the request for which modules should be shown
        emit_performance();
    });

    // Find out which modules should be shown given the current POS and Wordform
    $('#wordform').change(function () {
        // Emit the request for which modules should be shown
        emit_performance();
    });

    // Find out which modules should be shown given the current POS and Wordform
    $('#data_source').change(function () {
        toggle_pos_disabled(this.value);

        // Emit the request for which modules should be shown
        emit_performance();
    });

    // After successfully connecting to the Server
    socket.on('after connect', function (msg) {
        console.log('Successfully connected to server.');
    });

    // Getting which modules should be visible from the Server
    socket.on('output_performance', function (json) {
        let datasets = [];
        let i = 0;
        for (const [key, value] of Object.entries(json["performance"])) {
            datasets.push({
                // label: `From ${key.split(' ').map(word => word[0].toUpperCase() + word.substr(1)).join(' ')}`,
                label: `From ${wordform_to_human_readable[key]}`,
                data: value,
                backgroundColor: colors[i],
                borderWidth: 10,
                // barThickness: 50,

                categoryPercentage: 0.95,
                barPercentage: 1,
                // datalabels: {
                //     color: label_colors[i],
                // }
            })
            i++;
        }

        let data = {
            labels: json["labels"],
            datasets: datasets
        }

        // myChart.data.labels.pop();
        // myChart.data.datasets.forEach((dataset) => {
        //     dataset.data.pop();
        // });
        myChart.destroy();
        myChart = new Chart(ctx, {
            // Data is "to past"
            type: 'bar',
            data: data,
            options: options
        });
        // $("#chart").parent().css("width", `${json["labels"].length * 100}px`)
        $("#chart_title").html(`Accuracy of Python Modules when converting <b>${pos_to_human_readable_plural[$("#pos").val()]}</b> to <b>${wordform_to_human_readable[$("#wordform").val()]}</b> (${json['n_terms']} terms tested)`);
    });
});