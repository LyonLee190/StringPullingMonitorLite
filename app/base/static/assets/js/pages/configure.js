$(document).ready(function() {
    $("#upload").click(function() {
        var experiment_setting_id = document.getElementById("experiment_setting_id").value;
        var input_force = document.getElementById("input_force").value;
        var input_distance = document.getElementById("input_distance").value;
        var input_time_window = document.getElementById("input_time_window").value;

        var form_setting = new FormData();
        form_setting.append("experiment_setting_id", experiment_setting_id);
        form_setting.append("input_force", input_force);
        form_setting.append("input_distance", input_distance);
        form_setting.append("input_time_window", input_time_window);

        $.when(
            $.ajax({
                type : "POST",
                url : '/configure/upload',
                data : form_setting,
                dataType: "json",
                cache: false,
                processData: false,
                contentType: false,
                success : function(data) {
                    window.alert(data.msg);
                },
            })
        )
    })

    document.getElementById("experiment_setting_id").onchange = function() {
        var experiment_setting_id = document.getElementById("experiment_setting_id").value;

        var form_setting = new FormData();
        form_setting.append("experiment_setting_id", experiment_setting_id);

        $.when(
            $.ajax({
                type : "POST",
                url : '/configure/query',
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
            })
        )
    }
})
