$(document).ready(function() {
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

    document.getElementById("experiment_id").onchange = function() {
        var experiment_id = document.getElementById("experiment_id").value;
        var subject_id = document.getElementById("subject_id").value;

        var form_subject = new FormData();
        form_subject.append("experiment_id", experiment_id);
        form_subject.append("subject_id", subject_id);

        $.when(
            $.ajax({
                type : "POST",
                url : '/database/query/realtime_data',
                data : form_subject,
                dataType: "json",
                cache: false,
                processData: false,
                contentType: false,
                success : function(data) {
                    var time_stamp = data.time_stamp;
                    var pull_force = data.pull_force;
                    var pull_velocity = data.pull_velocity;
                    var pull_distance = data.pull_distance;
                    var completions = data.completions;

                    var content = "";
                    for (var i = 0; i < time_stamp.length; i++) {
                        content += "<tr>";
                        content += "<td>" + time_stamp[i] + "</td>" ;
                        content += "<td>" + pull_force[i] + "</td>" ;
                        content += "<td>" + pull_velocity[i] + "</td>" ;
                        content += "<td>" + pull_distance[i] + "</td>" ;
                        content += "<td>" + completions[i] + "</td>" ;
                        content += "</tr>";
                    }

                    document.getElementById("data_record").innerHTML = content;
                },
            })
        )
    }
})
