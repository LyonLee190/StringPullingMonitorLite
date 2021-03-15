$(document).ready(function() {

//    $("#setting_upload").click(function() {
//        var setting_id = document.getElementById("setting_id").value;
//        var input_force = document.getElementById("input_force").value;
//        var input_distance = document.getElementById("input_distance").value;
//        var input_time_window = document.getElementById("input_time_window").value;
//
//        var form_setting = new FormData();
//        form_setting.append("setting_id", setting_id);
//        form_setting.append("input_force", input_force);
//        form_setting.append("input_distance", input_distance);
//        form_setting.append("input_time_window", input_time_window);
//
//        $.when(
//            $.ajax({
//                type : "POST",
//                url : '/configure/upload',
//                data : form_setting,
//                dataType: "json",
//                cache: false,
//                processData: false,
//                contentType: false,
//                success : function(data) {
//                    if (!data.msg.equals("ValueError"))
//                        window.alert(data.msg);
//                },
//            })
//        )
//    })

    document.getElementById("subject_id").onchange = function() {
        var subject_id = document.getElementById("subject_id").value;

        var form_subject = new FormData();
        form_subject.append("subject_id", subject_id);

        $.when(
            $.ajax({
                type : "POST",
                url : '/database/query/experiment_id',
                data : form_subject,
                dataType: "json",
                cache: false,
                processData: false,
                contentType: false,
                success : function(data) {
                    var experiment_col = data.experiment_id;
                    for (var i = 0; i < experiment_col.length; i++) {
                        $("#experiment_id").append("<option>" + experiment_col[i] + "</option>");
                    }
                },
            })
        )
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
