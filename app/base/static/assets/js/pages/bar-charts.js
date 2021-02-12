'use strict';
$(document).ready(function() {
    setTimeout(function() {
    // [ bar-simple ] chart start
    var barChart = Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
                y: '2000',
                a: 70,
                b: 40,
                c: 30,
            },
            {
                y: '2009',
                a: 75,
                b: 65,
                c: 60,
            },
            {
                y: '2010',
                a: 50,
                b: 40,
                c: 55,
            },
            {
                y: '2011',
                a: 75,
                b: 65,
                c: 85,
            },
            {
                y: '2012',
                a: 100,
                b: 90,
                c: 40,
            }
        ],
        xkey: 'y',
        barSizeRatio: 0.70,
        barGap: 3,
        resize: true,
        responsive:true,
        ykeys: ['a', 'b', 'c'],
        labels: ['Bar 1', 'Bar 2', 'Bar 3'],
        barColors: ["0-#1de9b6-#1dc4e9", "0-#899FD4-#A389D4", "#04a9f5"]
    });
    // [ bar-simple ] chart end
        }, 700);
});
