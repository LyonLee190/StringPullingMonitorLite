'use strict';
$(document).ready(function() {
    var PULL_FORCE_MAX = 64;
    var pull_force = [{ label: "Pull Force", value: 0 }, { label: "Void", value: PULL_FORCE_MAX }];
    var PULL_VELOCITY_MAX = 64;
    var pull_velocity = [{ label: "Pull Velocity", value: 0 }, { label: "Void", value: PULL_VELOCITY_MAX }];
    var PULL_DISTANCE_MAX = 32;
    var pull_distance = [{ label: "Pull Distance", value: 0 }, { label: "Void", value: PULL_DISTANCE_MAX }];
    var TASKS_MAX = 16;
    var tasksN = [{ label: "Completed Tasks", value: 0 }, { label: "Void", value: TASKS_MAX }];

    var pull_force_donut = Morris.Donut({
        element: 'force-chart',
        data: pull_force,
        colors: ['#ef4f4f', '#f4f9f9'],
        resize: true,
        dataLabels: true,
        formatter: function (x) { return "Reading: " + x }
    });
    var pull_velocity_donut = Morris.Donut({
        element: 'velocity-chart',
        data: pull_velocity,
        colors: ['#ee9595', '#f4f9f9'],
        resize: true,
        dataLabels: true,
        formatter: function (x) { return "Reading: " + x }
    });
    var pull_distance_donut = Morris.Donut({
        element: 'distance-chart',
        data: pull_distance,
        colors: ['#ffcda3', '#f4f9f9'],
        resize: true,
        dataLabels: true,
        formatter: function (x) { return "Reading: " + x }
    });
    var tasksN_donut = Morris.Donut({
        element: 'n-tasks-chart',
        data: tasksN,
        colors: ['#74c7b8', '#f4f9f9'],
        resize: true,
        dataLabels: true,
        formatter: function (x) { return "Reading: " + x }
    });

    setInterval(function() {
//        alert("Hi there, Ajax");
        $.ajax({
            type: "POST",
            url: "/update",
            dataType: "json",
            success: function(data) {
                pull_force[0].value = data.force_val;
                pull_force[1].value = PULL_FORCE_MAX - data.force_val;
                pull_force_donut.setData(pull_force);
                pull_force_donut.select(0);

                pull_velocity[0].value = data.velocity_val;
                pull_velocity[1].value = PULL_VELOCITY_MAX - data.velocity_val;
                pull_velocity_donut.setData(pull_velocity);
                pull_velocity_donut.select(0);

                pull_distance[0].value = data.distance_val;
                pull_distance[1].value = PULL_DISTANCE_MAX - data.distance_val;
                pull_distance_donut.setData(pull_distance);
                pull_distance_donut.select(0);

                tasksN[0].value = data.tasks_val;
                tasksN[1].value = PULL_DISTANCE_MAX - data.tasks_val;
                tasksN_donut.setData(tasksN);
                tasksN_donut.select(0);
            }
        });
//        alert("Sayonara, Ajax");
    }, 3000);
});
