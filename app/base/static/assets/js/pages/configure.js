$(document).ready(function() {
    $("#info_submit").click(function() {
        var experiment_id = document.getElementById("experiment_id").value;
        var subject_id = document.getElementById("subject_id").value;
        var date = document.getElementById("date").value;
        var duration = document.getElementById("duration").value;
        var comment = document.getElementById("comment").value;
        var setting_id = document.getElementById("setting_id").value;

        var form_info = new FormData();
        form_info.append("experiment_id", experiment_id);
        form_info.append("subject_id", subject_id);
        form_info.append("date", date);
        form_info.append("duration", duration);
        form_info.append("comment", comment );
        form_info.append("setting_id", setting_id);

        $.ajax({
            type : "POST",
            url : '/configure/upload/experiment_info',
            data : form_info,
            dataType: "json",
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function() {
                window.alert("Start the Process");
            },
            success : function(data) {
                if (data.msg != "ValueError") {window.alert(data.msg);}
            },
        });
    })

    $("#setting_upload").click(function() {
        var setting_id = document.getElementById("setting_id").value;
        var input_force = document.getElementById("input_force").value;
        var input_distance = document.getElementById("input_distance").value;
        var input_time_window = document.getElementById("input_time_window").value;

        var form_setting = new FormData();
        form_setting.append("setting_id", setting_id);
        form_setting.append("input_force", input_force);
        form_setting.append("input_distance", input_distance);
        form_setting.append("input_time_window", input_time_window);

        $.ajax({
            type : "POST",
            url : '/configure/upload/configuration',
            data : form_setting,
            dataType: "json",
            cache: false,
            processData: false,
            contentType: false,
            success : function(data) {
                if (data.msg != "ValueError") {window.alert(data.msg);}
            },
        });
    })

    document.getElementById("setting_id").onchange = function() {
        var setting_id = document.getElementById("setting_id").value;

        var form_setting = new FormData();
        form_setting.append("setting_id", setting_id);

        $.ajax({
            type : "POST",
            url : '/configure/query/configuration',
            data : form_setting,
            dataType: "json",
            cache: false,
            processData: false,
            contentType: false,
            success : function(data) {
                document.getElementById("input_force").value = data.input_force;
                document.getElementById("input_distance").value = data.input_distance;
                document.getElementById("input_time_window").value = data.input_time_window;
            },
        });
    }

    var force = document.getElementById("input_force");
    force.min = "0";
    force.max = "64";
    force.step = "0.01";
    var distance = document.getElementById("input_distance");
    distance.min = "0";
    distance.max = "64";
    distance.step = "0.01";
    var time_window_r = document.getElementById("input_time_window");
    time_window_r.min = "0";
    time_window_r.max = "360";
    time_window_r.step = "1";
})
