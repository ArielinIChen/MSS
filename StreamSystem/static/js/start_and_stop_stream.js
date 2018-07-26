function create_stream_info_table(received_value, i) {
    var html = '';
    html += '<tr>';
    html += '<td class="stream_method_bgcolor_css" style="color: white" class="col-lg-2"><font size="3">';
    html += received_value[i].stream_method + '</font></td>';
    html += '<td><font size="3">' + received_value[i].channel_name + '</font></td>' +
        '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + received_value[i].src_path + '</font></td>' +
        '<td style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"><font size="3">' + received_value[i].dst_path + '</font></td>' +
        '<td><font size="3">' + received_value[i].create_time + '</font></td>' +
        '<td>' + '<form role="form" id="stream_stop_' + received_value[i].channel_name + '">' +
        '<input type="hidden" name="channel_name" value="' + received_value[i].channel_name + '">' + '</form>';
    html += '<button type="submit" class="btn btn-default" id="stream_stop">Stop</button>';
    html += '</td>' + '</tr>';

    return html
}

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
                html += create_stream_info_table(received_value, i);
            }
        }
        else if (received_value[i].stream_method === 'relay') {
            if (method_var === 'all' || method_var === 'relay') {
                html += create_stream_info_table(received_value, i);
            }
        }
        else if (received_value[i].stream_method === 'publish') {
            if (method_var === 'all' || method_var === 'publish') {
                html += create_stream_info_table(received_value, i);
            }
        }
        else {
            if (method_var === 'all') {
                html += create_stream_info_table(received_value, i);
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

function stream_tag_color() {
    var tdArr = document.getElementsByClassName('stream_method_bgcolor_css');
    for (var j = 0; j < tdArr.length; j++) {
        console.log(tdArr[j].innerText);
        if (tdArr[j].innerText === 'streamlink') {
            tdArr[j].style.backgroundColor = 'darkgreen'
        }
        else if (tdArr[j].innerText === 'relay') {
            tdArr[j].style.backgroundColor = 'orangered'
        }
        else if (tdArr[j].innerText === 'publish') {
            tdArr[j].style.backgroundColor = 'cornflowerblue';
        }
    }
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
                stream_tag_color();

                $("p#p_filter_all").click(function () {
                    p_filter_click(res, 'all');
                    stream_tag_color();
                });

                $("p#p_filter_streamlink").click(function () {
                    p_filter_click(res, 'streamlink');
                    $('.stream_method_bgcolor_css').css('background-color', 'darkgreen');
                });

                $("p#p_filter_relay").click(function () {
                    p_filter_click(res, 'relay');
                    $('.stream_method_bgcolor_css').css('background-color', 'orangered');
                });

                $("p#p_filter_publish").click(function () {
                    p_filter_click(res, 'publish');
                    $('.stream_method_bgcolor_css').css('background-color', 'cornflowerblue');
                });
            }
            else {
                document.getElementById("stream_info").innerHTML='<p>Nothing to show</p>';
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
                alert(err['responseJSON']['error']);
            }
        })
    })
});
