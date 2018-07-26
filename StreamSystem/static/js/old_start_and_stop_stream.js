function p_filter_click(received_value, method_var) {
    var html = '';
    html += '<table class="table table-hover" style="table-layout:fixed" id="now_streaming_table">';
    html += '<thead><tr>' +
        '<th class="col-lg-2">Stream Method</th>' +
        '<th class="col-lg-3">Channel Name</th>' +
        '<th class="col-lg-7">Source Path</th>' +
        '<th class="col-lg-7">Dest Path</th>' +
        '<th class="col-lg-3">Create Time</th>' +
        '<th class="col-lg-2">Choice</th>' +
        '</tr></thead><tbody>';
    for (var i = 1; i < received_value.length; i++) {
        if (received_value[i].stream_method === 'streamlink') {
            if (method_var === 'all' || method_var === 'streamlink') {
                html += '<tr>';
                html += '<td bgcolor=darkgreen class="col-lg-2"><font size="3">';
                html += received_value[i].stream_method + '</font></td>';
                html += '<td id="td_' + received_value[i].channel_name + '"><font size="3">' + received_value[i].channel_name + '</font></td>' +
                    '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + received_value[i].src_path + '</font></td>' +
                    '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + received_value[i].dst_path + '</font></td>' +
                    '<td><font size="3">' + received_value[i].create_time + '</font></td>' +
                    '<td>' + '<form role="form" id="stream_stop_' + received_value[i].channel_name + '">' +
                    '<input type="hidden" name="channel_name" value="' + received_value[i].channel_name + '">' + '</form>';
                html += '<button type="submit" class="btn btn-default" style="background-color: darkgreen; color: white;" id="stream_stop">Stop</button>';
                html += '</td>' + '</tr>';
            }
        }
        else if (received_value[i].stream_method === 'relay') {
            if (method_var === 'all' || method_var === 'relay') {
                html += '<tr>';
                html += '<td bgcolor=orangered class="col-lg-2"><font size="3">';
                html += received_value[i].stream_method + '</font></td>';
                html += '<td id="td_' + received_value[i].channel_name + '"><font size="3">' + received_value[i].channel_name + '</font></td>' +
                    '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + received_value[i].src_path + '</font></td>' +
                    '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + received_value[i].dst_path + '</font></td>' +
                    '<td><font size="3">' + received_value[i].create_time + '</font></td>' +
                    '<td>' + '<form role="form" id="stream_stop_' + received_value[i].channel_name + '">' +
                    '<input type="hidden" name="channel_name" value="' + received_value[i].channel_name + '">' + '</form>';
                html += '<button type="submit" class="btn btn-default" style="background-color: orangered; color: white;" id="stream_stop">Stop</button>';
                html += '</td>' + '</tr>';
            }
        }
        else if (received_value[i].stream_method === 'publish') {
            if (method_var === 'all' || method_var === 'publish') {
                html += '<tr>';
                html += '<td bgcolor=cornflowerblue class="col-lg-2"><font size="3">';
                html += received_value[i].stream_method + '</font></td>';
                html += '<td id="td_' + received_value[i].channel_name + '"><font size="3">' + received_value[i].channel_name + '</font></td>' +
                    '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + received_value[i].src_path + '</font></td>' +
                    '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + received_value[i].dst_path + '</font></td>' +
                    '<td><font size="3">' + received_value[i].create_time + '</font></td>' +
                    '<td>' + '<form role="form" id="stream_stop_' + received_value[i].channel_name + '">' +
                    '<input type="hidden" name="channel_name" value="' + received_value[i].channel_name + '">' + '</form>';
                html += '<button type="submit" class="btn btn-default" style="background-color: cornflowerblue; color: white;" id="stream_stop">Stop</button>';
                html += '</td>' + '</tr>';
            }
        }
        else {
            if (method_var === 'all') {
                html += '<tr>';
                html += '<td bgcolor=white class="col-lg-2"><font size="3">';
                html += received_value[i].stream_method + '</font></td>';
                html += '<td id="td_' + received_value[i].channel_name + '"><font size="3">' + received_value[i].channel_name + '</font></td>' +
                    '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + received_value[i].src_path + '</font></td>' +
                    '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + received_value[i].dst_path + '</font></td>' +
                    '<td><font size="3">' + received_value[i].create_time + '</font></td>' +
                    '<td>' + '<form role="form" id="stream_stop_' + received_value[i].channel_name + '">' +
                    '<input type="hidden" name="channel_name" value="' + received_value[i].channel_name + '">' + '</form>';
                html += '<button type="submit" class="btn btn-default" id="stream_stop">Stop</button>';
                html += '</td>' + '</tr>';
            }
        }
    }
    html += '</tbody></table>';
    document.getElementById("stream_info").innerHTML=html;
    // $("div#stream_info").html(html);
    $("button#stream_stop").click(function () {
        var element = $(this).closest('tr').find('td').eq(1).text();
        console.log(element);
        stop_stream_click(element);
    });
}

function stop_stream_click(element) {
    // var element = $(this).closest('tr').find('td').eq(1).text();
    // console.log(element);
    var post_data = JSON.stringify({"channel_name": element});
    console.log(post_data);
    $.ajax({
        type: 'post',
        url: '/stream/del/',
        dataType: 'json',
        data: post_data,
        headers: {"X-CSRFtoken": Cookies.get("csrftoken")},
        success: function (res) {
            console.log(res);
            alert(res['success']);
            window.location.replace(location.href);
        },
        error: function (err) {
            console.log(err);
            alert(err['error']);
        }
    })
}

$(document).ready(function ShowStreamsInDb() {
    $.ajax({
        type: 'get',
        url: '/show_stream/',
        dataType: 'json',
        success: function(res) {
            console.log(res);
            if (res[0] === 'Filled') {
                p_filter_click(res, 'all');
                // var html = '';
                // html += '<table class="table table-hover" style="table-layout:fixed" id="now_streaming_table">';
                // html += '<thead><tr>' +
                //     '<th class="col-lg-2">Stream Method</th>' +
                //     '<th class="col-lg-3">Channel Name</th>' +
                //     '<th class="col-lg-7">Source Path</th>' +
                //     '<th class="col-lg-7">Dest Path</th>' +
                //     '<th class="col-lg-3">Create Time</th>' +
                //     '<th class="col-lg-2">Choice</th>' +
                //     '</tr></thead><tbody>';
                // for (var i = 1; i < res.length; i++) {
                //     html += '<tr>';
                //     if (res[i].stream_method === 'streamlink') {
                //         html += '<td bgcolor=darkgreen class="col-lg-2">';
                //     }
                //     else if (res[i].stream_method === 'relay') {
                //         html += '<td bgcolor=orangered class="col-lg-2">';
                //     }
                //     else if (res[i].stream_method === 'publish') {
                //         html += '<td bgcolor=cornflowerblue class="col-lg-2">';
                //     }
                //     else {
                //         html += '<td bgcolor=white class="col-lg-2"><font size="3">';
                //     }
                //     html += res[i].stream_method + '</font></td>';
                //     html += '<td id="td_' + res[i].channel_name + '"><font size="3">' + res[i].channel_name + '</font></td>' +
                //         '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + res[i].src_path + '</font></td>' +
                //         '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + res[i].dst_path + '</font></td>' +
                //         '<td><font size="3">' + res[i].create_time + '</font></td>' +
                //         '<td>' + '<form role="form" id="stream_stop_' + res[i].channel_name + '">' +
                //         '<input type="hidden" name="channel_name" value="' + res[i].channel_name + '">' + '</form>';
                //     if (res[i].stream_method === 'streamlink') {
                //         html += '<button type="submit" class="btn btn-default" style="background-color: darkgreen; color: white;" id="stream_stop">Stop</button>';
                //     }
                //     else if (res[i].stream_method === 'relay') {
                //         html += '<button type="submit" class="btn btn-default" style="background-color: orangered; color: white;" id="stream_stop">Stop</button>';
                //     }
                //     else if (res[i].stream_method === 'publish') {
                //         html += '<button type="submit" class="btn btn-default" style="background-color: cornflowerblue; color: white;" id="stream_stop">Stop</button>';
                //     }
                //     else {
                //         html += '<button type="submit" class="btn btn-default" id="stream_stop">Stop</button>';
                //     }
                //     html += '</td>' + '</tr>';
                // }
                // html += '</tbody></table>';
                // $("div#stream_info").html(html);
                //
                // $("button#stream_stop").click(function () {
                //     var element = $(this).closest('tr').find('td').eq(1).text();
                //     console.log(element);
                //     stop_stream_click(element);
                // });

                $("p#p_filter_all").click(function () {
                    p_filter_click(res, 'all');
                    // var html = '';
                    // html += '<table class="table table-hover" style="table-layout:fixed" id="now_streaming_table">';
                    // html += '<thead><tr>' +
                    //     '<th class="col-lg-2">Stream Method</th>' +
                    //     '<th class="col-lg-3">Channel Name</th>' +
                    //     '<th class="col-lg-7">Source Path</th>' +
                    //     '<th class="col-lg-7">Dest Path</th>' +
                    //     '<th class="col-lg-3">Create Time</th>' +
                    //     '<th class="col-lg-2">Choice</th>' +
                    //     '</tr></thead><tbody>';
                    // for (var i = 1; i < res.length; i++) {
                    //     html += '<tr>';
                    //     if (res[i].stream_method === 'streamlink') {
                    //         html += '<td bgcolor=darkgreen class="col-lg-2">';
                    //     }
                    //     else if (res[i].stream_method === 'relay') {
                    //         html += '<td bgcolor=orangered class="col-lg-2">';
                    //     }
                    //     else if (res[i].stream_method === 'publish') {
                    //         html += '<td bgcolor=cornflowerblue class="col-lg-2">';
                    //     }
                    //     else {
                    //         html += '<td bgcolor=white class="col-lg-2"><font size="3">';
                    //     }
                    //     html += res[i].stream_method + '</font></td>';
                    //     html += '<td id="td_' + res[i].channel_name + '"><font size="3">' + res[i].channel_name + '</font></td>' +
                    //         '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + res[i].src_path + '</font></td>' +
                    //         '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + res[i].dst_path + '</font></td>' +
                    //         '<td><font size="3">' + res[i].create_time + '</font></td>' +
                    //         '<td>' + '<form role="form" id="stream_stop_' + res[i].channel_name + '">' +
                    //         '<input type="hidden" name="channel_name" value="' + res[i].channel_name + '">' + '</form>';
                    //     if (res[i].stream_method === 'streamlink') {
                    //         html += '<button type="submit" class="btn btn-default" style="background-color: darkgreen; color: white;" id="stream_stop">Stop</button>';
                    //     }
                    //     else if (res[i].stream_method === 'relay') {
                    //         html += '<button type="submit" class="btn btn-default" style="background-color: orangered; color: white;" id="stream_stop">Stop</button>';
                    //     }
                    //     else if (res[i].stream_method === 'publish') {
                    //         html += '<button type="submit" class="btn btn-default" style="background-color: cornflowerblue; color: white;" id="stream_stop">Stop</button>';
                    //     }
                    //     else {
                    //         html += '<button type="submit" class="btn btn-default" id="stream_stop">Stop</button>';
                    //     }
                    //     html += '</td>' + '</tr>';
                    // }
                    // html += '</tbody></table>';
                    // document.getElementById("stream_info").innerHTML=html;
                    //
                    // $("button#stream_stop").click(function () {
                    //     var element = $(this).closest('tr').find('td').eq(1).text();
                    //     console.log(element);
                    //     stop_stream_click(element);
                    // });
                });

                $("p#p_filter_streamlink").click(function () {
                    p_filter_click(res, 'streamlink');
                    // var html = '';
                    // html += '<table class="table table-hover" style="table-layout:fixed" id="now_streaming_table">';
                    // html += '<thead><tr>' +
                    //     '<th class="col-lg-2">Stream Method</th>' +
                    //     '<th class="col-lg-3">Channel Name</th>' +
                    //     '<th class="col-lg-7">Source Path</th>' +
                    //     '<th class="col-lg-7">Dest Path</th>' +
                    //     '<th class="col-lg-3">Create Time</th>' +
                    //     '<th class="col-lg-2">Choice</th>' +
                    //     '</tr></thead><tbody>';
                    // for (var i = 1; i < res.length; i++) {
                    //     if (res[i].stream_method === 'streamlink') {
                    //         html += '<tr>';
                    //         html += '<td bgcolor=darkgreen class="col-lg-2">';
                    //         html += res[i].stream_method + '</font></td>';
                    //         html += '<td id="td_' + res[i].channel_name + '"><font size="3">' + res[i].channel_name + '</font></td>' +
                    //             '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + res[i].src_path + '</font></td>' +
                    //             '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + res[i].dst_path + '</font></td>' +
                    //             '<td><font size="3">' + res[i].create_time + '</font></td>' +
                    //             '<td>' + '<form role="form" id="stream_stop_' + res[i].channel_name + '">' +
                    //             '<input type="hidden" name="channel_name" value="' + res[i].channel_name + '">' + '</form>';
                    //         html += '<button type="submit" class="btn btn-default" style="background-color: darkgreen; color: white;" id="stream_stop">Stop</button>';
                    //         html += '</td>' + '</tr>';
                    //     }
                    // }
                    // html += '</tbody></table>';
                    // document.getElementById("stream_info").innerHTML=html;
                    //
                    // $("button#stream_stop").click(function () {
                    //     var element = $(this).closest('tr').find('td').eq(1).text();
                    //     console.log(element);
                    //     stop_stream_click(element);
                    // });
                });

                $("p#p_filter_relay").click(function () {
                    p_filter_click(res, 'relay');
                    // var html = '';
                    // html += '<table class="table table-hover" style="table-layout:fixed" id="now_streaming_table">';
                    // html += '<thead><tr>' +
                    //     '<th class="col-lg-2">Stream Method</th>' +
                    //     '<th class="col-lg-3">Channel Name</th>' +
                    //     '<th class="col-lg-7">Source Path</th>' +
                    //     '<th class="col-lg-7">Dest Path</th>' +
                    //     '<th class="col-lg-3">Create Time</th>' +
                    //     '<th class="col-lg-2">Choice</th>' +
                    //     '</tr></thead><tbody>';
                    // for (var i = 1; i < res.length; i++) {
                    //     if (res[i].stream_method === 'relay') {
                    //         html += '<tr>';
                    //         html += '<td bgcolor=orangered class="col-lg-2">';
                    //         html += res[i].stream_method + '</font></td>';
                    //         html += '<td id="td_' + res[i].channel_name + '"><font size="3">' + res[i].channel_name + '</font></td>' +
                    //             '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + res[i].src_path + '</font></td>' +
                    //             '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + res[i].dst_path + '</font></td>' +
                    //             '<td><font size="3">' + res[i].create_time + '</font></td>' +
                    //             '<td>' + '<form role="form" id="stream_stop_' + res[i].channel_name + '">' +
                    //             '<input type="hidden" name="channel_name" value="' + res[i].channel_name + '">' + '</form>';
                    //         html += '<button type="submit" class="btn btn-default" style="background-color: orangered; color: white;" id="stream_stop">Stop</button>';
                    //         html += '</td>' + '</tr>';
                    //     }
                    // }
                    // html += '</tbody></table>';
                    // document.getElementById("stream_info").innerHTML=html;
                    //
                    // $("button#stream_stop").click(function () {
                    //     var element = $(this).closest('tr').find('td').eq(1).text();
                    //     console.log(element);
                    //     stop_stream_click(element);
                    // });
                });

                $("p#p_filter_publish").click(function () {
                    p_filter_click(res, 'publish');
                    // var html = '';
                    // html += '<table class="table table-hover" style="table-layout:fixed" id="now_streaming_table">';
                    // html += '<thead><tr>' +
                    //     '<th class="col-lg-2">Stream Method</th>' +
                    //     '<th class="col-lg-3">Channel Name</th>' +
                    //     '<th class="col-lg-7">Source Path</th>' +
                    //     '<th class="col-lg-7">Dest Path</th>' +
                    //     '<th class="col-lg-3">Create Time</th>' +
                    //     '<th class="col-lg-2">Choice</th>' +
                    //     '</tr></thead><tbody>';
                    // for (var i = 1; i < res.length; i++) {
                    //     if (res[i].stream_method === 'publish') {
                    //         html += '<tr>';
                    //         html += '<td bgcolor=cornflowerblue class="col-lg-2">';
                    //         html += res[i].stream_method + '</font></td>';
                    //         html += '<td id="td_' + res[i].channel_name + '"><font size="3">' + res[i].channel_name + '</font></td>' +
                    //             '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + res[i].src_path + '</font></td>' +
                    //             '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + res[i].dst_path + '</font></td>' +
                    //             '<td><font size="3">' + res[i].create_time + '</font></td>' +
                    //             '<td>' + '<form role="form" id="stream_stop_' + res[i].channel_name + '">' +
                    //             '<input type="hidden" name="channel_name" value="' + res[i].channel_name + '">' + '</form>';
                    //         html += '<button type="submit" class="btn btn-default" style="background-color: cornflowerblue; color: white;" id="stream_stop">Stop</button>';
                    //         html += '</td>' + '</tr>';
                    //     }
                    // }
                    // html += '</tbody></table>';
                    // document.getElementById("stream_info").innerHTML=html;
                    //
                    // $("button#stream_stop").click(function () {
                    //     var element = $(this).closest('tr').find('td').eq(1).text();
                    //     console.log(element);
                    //     stop_stream_click(element);
                    // });
                });
            }
        },
        error: function(err) {
            console.log(err['error']);
        }
    });
    $('button#add_stream_btn').click(function () {
        var mytext = $('form#add_stream_form').serializeArray();
        var mydict = {};
        for (var x in mytext) {
            mydict[mytext[x].name] = mytext[x].value;
        }
        console.log(mydict);
        $.ajax({
            type: 'post',
            url: '/stream/add/',
            dataType: 'json',
            data: JSON.stringify(mydict),
            headers: {"X-CSRFtoken": Cookies.get("csrftoken")},
            success: function (res) {
                console.log(res);
                alert(res['success']);
                window.location.replace(location.href);
            },
            error: function (err) {
                console.log(err);
                alert(err['error']);
            }
        })
    })
});
