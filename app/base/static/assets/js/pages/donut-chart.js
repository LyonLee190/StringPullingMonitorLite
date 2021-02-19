'use strict';
$(document).ready(function() {
    var LOAD_CELL_MAX = 64;
    var load_cell = [{ label: "Load Cell", value: 0 }, { label: "Void", value: LOAD_CELL_MAX }];
    var OPTICAL_SENSOR_MAX = 64;
    var optical_sensor_1 = [{ label: "Optical Sensor 1", value: 0 }, { label: "Void", value: OPTICAL_SENSOR_MAX }];
    var optical_sensor_2 = [{ label: "Optical Sensor 2", value: 0 }, { label: "Void", value: OPTICAL_SENSOR_MAX }];

    var load_cell_donut = Morris.Donut({
        element: 'LC-chart',
        data: load_cell,
        colors: ['#ef4f4f', '#f4f9f9'],
        resize: true,
        dataLabels: true,
        formatter: function (x) { return "Reading: " + x }
    });
    var optical_sensor_1_donut = Morris.Donut({
        element: 'OS-1-chart',
        data: optical_sensor_1,
        colors: ['#ee9595', '#f4f9f9'],
        resize: true,
        dataLabels: true,
        formatter: function (x) { return "Reading: " + x }
    });
    var optical_sensor_2_donut = Morris.Donut({
        element: 'OS-2-chart',
        data: optical_sensor_2,
        colors: ['#ffcda3', '#f4f9f9'],
        resize: true,
        dataLabels: true,
        formatter: function (x) { return "Reading: " + x }
    });

    setInterval(function() {
//        alert("Hi there, Ajax");
        $.ajax({
            type: "POST",
            url: "/sensor_data_update",
            dataType: "json",
            success: function(data) {
                load_cell[0].value = data.LC_val;
                load_cell[1].value = LOAD_CELL_MAX - data.LC_val;
                load_cell_donut.setData(load_cell);
                load_cell_donut.select(0);

                optical_sensor_1[0].value = data.OS_1_val;
                optical_sensor_1[1].value = OPTICAL_SENSOR_MAX - data.OS_1_val;
                optical_sensor_1_donut.setData(optical_sensor_1);
                optical_sensor_1_donut.select(0);

                optical_sensor_2[0].value = data.OS_2_val;
                optical_sensor_2[1].value = OPTICAL_SENSOR_MAX - data.OS_2_val;
                optical_sensor_2_donut.setData(optical_sensor_2);
                optical_sensor_2_donut.select(0);
            }
        });
//        alert("Sayonara, Ajax");
    }, 1000);
});
