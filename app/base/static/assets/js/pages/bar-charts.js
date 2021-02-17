'use strict';
$(document).ready(function() {
//    setTimeout(function() {
    // [ bar-simple ] chart start
    var barChart = Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
                y: 'Subject ID',
                a: 2,
                b: 4,
                c: 8,
                d: 16,
                e: 32
            }
        ],
        xkey: 'y',
        barSizeRatio: 0.70,
        barGap: 3,
        resize: true,
        responsive:true,
        ykeys: ['a', 'b', 'c', 'd', 'e'],
        labels: ['Pull Force', 'Pull Velocity', 'Pull Distance', 'Time Elapsed' ,'Completed Task'],
        barColors: ["#ED5752", "#92AAC7", "#E2DFA2", "#A1BE95", "#B3DE81"]
    });
    // [ bar-simple ] chart end
//        }, 700);

//    var interval_id = setInterval(update_values, 1000);
//    var result;
//    function update_values() {
//        $.getJSON($SCRIPT_ROOT + '/data_retrieve',
//        function(data) {result = data;})
//    }
        setInterval(function() {
//                var result;
//                $.getJSON($SCRIPT_ROOT + '/data_retrieve',
//                function(data) {
//                    result = data;
//                }));
//
//                barChart.data[0].y[0] = result;
//                barChart.data[0].y[3] += 1;
                barChart.update();
        }, 1000);
});
