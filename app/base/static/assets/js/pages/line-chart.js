'use strict';
$(document).ready(function() {
    var current = new Date();
    var pull_force = [{ time: current.getTime(), value: 0 }];
    var pull_velocity = [{ time: current.getTime(), value: 0 }];
    var pull_distance = [{ time: current.getTime(), value: 0 }];
    var completions = [{ time: current.getTime(), value: 0 }];

    var force_chart = Morris.Line({
        element: 'force-chart',
        data: pull_force,
        lineColors: ['#ef4f4f'],
        xkey: 'time',
        ykeys: ['value'],
        labels: ['Pull Force'],
        redraw: true,
        resize: true,
        responsive:true,
        hideHover: 'auto'
    });
    var velocity_chart = Morris.Line({
        element: 'velocity-chart',
        data: pull_velocity,
        lineColors: ['#ee9595'],
        xkey: 'time',
        ykeys: ['value'],
        labels: ['Pull Velocity'],
        redraw: true,
        resize: true,
        responsive:true,
        hideHover: 'auto'
    });
    var distance_chart = Morris.Line({
        element: 'distance-chart',
        data: pull_distance,
        lineColors: ['#ffcda3'],
        xkey: 'time',
        ykeys: ['value'],
        labels: ['Pull Distance'],
        redraw: true,
        resize: true,
        responsive:true,
        hideHover: 'auto'
    });
    var completions_chart = Morris.Line({
        element: 'completions-chart',
        data: completions,
        lineColors: ['#74c7b8'],
        xkey: 'time',
        ykeys: ['value'],
        labels: ['Pull Distance'],
        redraw: true,
        resize: true,
        responsive:true,
        hideHover: 'auto'
    });

    setInterval(function() {
//        alert("Hi there, Ajax");
        $.ajax({
            type: "POST",
            url: "/real_time_data_update",
            dataType: "json",
            success: function(data) {
            current = new Date();
                if (pull_force.length == 30) {
                    pull_force.shift();
                    pull_velocity.shift();
                    pull_distance.shift();
                    completions.shift();
                }

                pull_force.push({ time: current.getTime(), value: data.force_val });
                force_chart.setData(pull_force);
                pull_velocity.push({ time: current.getTime(), value: data.velocity_val });
                velocity_chart.setData(pull_velocity);
                pull_distance.push({ time: current.getTime(), value: data.distance_val });
                distance_chart.setData(pull_distance);
                completions.push({ time: current.getTime(), value: data.completions_val });
                completions_chart.setData(completions);
            }
        });
//        alert("Sayonara, Ajax");
    }, 1000);
});
