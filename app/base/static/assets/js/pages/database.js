$(document).ready(function() {
    document.getElementById("subject_id").onchange = function() {
        var subject_id = document.getElementById("subject_id").value;

        var form_subject = new FormData();
        form_subject.append("subject_id", subject_id);

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
        });
    }

    document.getElementById("experiment_id").onchange = function() {
        var experiment_id = document.getElementById("experiment_id").value;
        var subject_id = document.getElementById("subject_id").value;

        var form_subject = new FormData();
        form_subject.append("experiment_id", experiment_id);
        form_subject.append("subject_id", subject_id);

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
                    content += "<td>" + time_stamp[i].split(",")[1] + "</td>" ;
                    content += "<td>" + pull_force[i] + "</td>" ;
                    content += "<td>" + pull_velocity[i] + "</td>" ;
                    content += "<td>" + pull_distance[i] + "</td>" ;
                    content += "<td>" + completions[i] + "</td>" ;
                    content += "</tr>";
                }

                document.getElementById("data_record").innerHTML = content;
            },
        });
    }

    $("#download").click(function(e) {
        download_table_as_csv("metadata");
    });

    $("#delete").click(function(e) {
        var experiment_id = document.getElementById("experiment_id").value;
        var subject_id = document.getElementById("subject_id").value;

        var form_subject = new FormData();
        form_subject.append("experiment_id", experiment_id);
        form_subject.append("subject_id", subject_id);

        $.ajax({
            type : "POST",
            url : '/database/delete/record',
            data : form_subject,
            dataType: "json",
            cache: false,
            processData: false,
            contentType: false,
            success : function(data) {
                window.alert(data.msg);
            },
        });
    });
});

// https://stackoverflow.com/questions/15547198/export-html-table-to-csv
// Quick and simple export target #table_id into a csv
function download_table_as_csv(table_id, separator = ',') {
    // Select rows from table_id
    var rows = document.querySelectorAll('table#' + table_id + ' tr');
    // Construct csv
    var csv = [];
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        for (var j = 0; j < cols.length; j++) {
            // Clean innertext to remove multiple spaces and jumpline (break csv)
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
            // Push escaped string
            row.push(data);
        }
        csv.push(row.join(separator));
    }
    var csv_string = csv.join('\n');

    var experiment_id = document.getElementById("experiment_id").value;
    var subject_id = document.getElementById("subject_id").value;
    // Download it
    var filename = experiment_id + '_' + subject_id + '.csv';
    var link = document.createElement('a');
    link.style.display = 'none';
    link.setAttribute('target', '_blank');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
