/* 

THIS CODE CONTAINS MODIFIED CODE FROM LAB 08

*/
$(document).ready(function() {
    //this will update the capture_sessions table in html on refresh click
    $('#refresh-button').click(function () {
        $("#capture-sessions").empty();
        
        $.ajax({
            url: "/getSessionsData",
            type: "GET",
            dataType: "json",
            success: function(response) {
                $("#captures-table").html("");
                var sessions = [];
                for (var i in response) {
                    var data_list = response[i];
                    var session = {
                        id: data_list[0],
                        capture_id: data_list[1],
                        insertion_datetime: data_list[2]
                    };
                    sessions.push(session);
                }
                
                // put data gathered into new table row in frisberry html file
                for (var i in sessions) {
                    var session = sessions[i];
                    $("<tr data-capture-session='" + session.capture_id + "'>" +
                        "<td>" + session.id + "</td>" +
                        "<td>" + session.capture_id + "</td>" +
                        "<td>" + session.insertion_datetime + "</td>" +
                    "</tr>").appendTo($("#capture-sessions"));
                }

            }
            
        });
    });

    //when a specific capture is clicked, this updates the table on the webpage
    $(document).on("click", "#capture-sessions tr", function () {
        var captureSession = $(this).data("capture-session");
        $.ajax({
            url: "/getCaptureData",
            type: "GET",
            data: {capture_session: captureSession},
            dataType: "json",
            success: function(response) {
                var accel_datas = [];
                for (var i in response) {
                    var data_list = response[i];
                    var accel_data = {
                        id: data_list[0],
                        capture_session: data_list[1],
                        time_from_start: data_list[2],
                        mag_accel: data_list[3],
                        mag_gyro: data_list[4]
                    };
                    accel_datas.push(accel_data);
                }

                tableRows = "";
                for (var i in accel_datas) {
                    var capture = accel_datas[i];

                    tableRows += ("<tr data-capture-session='" + capture.capture_session + "'>" +
                                 "<td>" + capture.id + "</td>" +
                                 "<td>" + capture.capture_session + "</td>" +
                                 "<td>" + capture.time_from_start + "</td>" +
                                 "<td>" + capture.mag_accel + "</td>" +
                                 "<td>" + capture.mag_gyro + "</td>" +
                                 "</tr>")
                }

                $("#captures-table").html(tableRows);
            }
        });
    });
});
