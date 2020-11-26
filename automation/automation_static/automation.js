function init_team_project(form) {
    // 加载团队team

    // type指数据库集合
    http('/variable/api/v1/aggregate', 'post', {type: 'team', key: 'team'},
        function (response) {
            // option动态拼接
            // 先拼接team
            let teamData = response['data'];
            let html = '';
            for (index in teamData) {
                let value = teamData[index]['_id'];
                html += `<option value="${value}">${value}</option>`;
            }
            $('#team').append(html);
            // 再拼接project
            let team;
            for (index in teamData) {
                team = teamData[index]['_id'];
                break; // 循环只执行一次，获取第一个team值，便于加载页面时的默认project拼接
            }
            http('/variable/api/v1/searchProject', 'post', {"type": 'team', "team": team},
                function (response) {
                    let projectData = response['data'];
                    let html = '';
                    for (index in projectData) {
                        let value = projectData[index]['project'];
                        html += `<option value="${value}">${value}</option>`;
                    }
                    $('#project').append(html);
                    // 表单html改变需要手动render
                    form.render();
                }, function (response) {
                    console.log(response);
                });
        }, function (response) {
            console.log(response)
        }
    )
}

function addOperationLine(form) {
    $(document).on("click", '#add', function () {
        let html = '<div class="layui-form-item op-line">' +
            '<div class="layui-inline">' +
            '<div class="layui-input-inline" style="width:120px">' +
            '<select name="op-type" class="op-type">' +
            '<option value="get_url">打开</option>' +
            '<option value="click_element">点击</option>' +
            '<option value="wait">等待</option>' +
            '<option value="input_content">输入</option>' +
            '<option value="page_should_contain">断言</option>' +
            '<option value="switch_iframe">切换iframe</option>' +
            '<option value="switch_window">切换window</option>' +
            '</select>' +
            '</div>' +
            '<div class="layui-input-inline">' +
            '<select name="op-by" class="op-by">' +
            '<option value="id">ID</option>' +
            '<option value="xpath">XPATH</option>' +
            '<option value="link text">LINK_TEXT</option>' +
            '<option value="partial link text">PARTIAL_LINK_TEXT</option>' +
            '<option value="name">NAME</option>' +
            '<option value="tag name">TAG_NAME</option>' +
            '<option value="class name">CLASS_NAME</option>' +
            '<option value="css selector">CSS_SELECTOR</option>' +
            '</select>' +
            '</div>' +
            '<div class="layui-input-inline" style="width:300px">' +
            '<input type="text" class="layui-input locator" placeholder="请输入定位器">' +
            '</div>' +
            '<div class="layui-input-inline" style="width:300px">' +
            '<input type="text" class="layui-input op-data" required ' +
            'lay-verify="required" placeholder="请输入测试数据">' +
            '</div>' +
            '</div>' +
            '<div class="layui-inline">' +
            '<input type="button" class="layui-btn move-up" value="上移">' +
            '<input type="button" class="layui-btn layui-btn-normal move-down" value="下移">' +
            '<input type="button" class="layui-btn layui-btn-danger delete-line" value="删除">' +
            '<input type="button" class="layui-btn layui-btn-primary lock-line" value="锁定">' +
            '</div>' +
            '<div class="layui-inline">' +
            '<i class="op-result" style="font-size:30px; display:none"></i>' +
            '</div>' +
            '</div>' +
            '</div>';
        let section = $('#script');
        section.append(html);
        section.show();
        form.render();
    })
}

function refresh_result(result_list) {
    let icon = $('i.op-result');
    icon.removeClass();
    for (index in result_list) {
        let dom = icon.eq(index);
        if (result_list[index]) {
            dom.addClass('layui-icon layui-icon-ok-circle');
            dom.css('color', '#5FB878');
        } else {
            dom.addClass('layui-icon layui-icon-close');
            dom.css('color', '#FF5722');
            break;
        }
    }
    icon.show();

}

function deleteOperationLine() {
    let dom = $('#script');
    dom.on('click', '.delete-line', function () {
        let i = $('.delete-line').index($(this));
        $('.op-line').eq(i).remove();
    })
}

function getOperationInfo() {
    let operation = [];
    let dom = $('div.op-line');
    dom.each(function (index, element) {
        let op = {
            'type': $('select.op-type').eq(index).val(),
            'by': $('select.op-by').eq(index).val(),
            'locator': $('input.locator').eq(index).val(),
            'data': $('input.op-data').eq(index).val()
        };
        operation.push(op);
    });
    return operation;
}

function run(layer) {
    $('#run').click(function () {
        let data = getOperationInfo();
        http('/automation/api/v1/run', 'post', data, function (response) {
            if (response['data']['test_result'] === true) {
                layer.msg('测试结果：成功');
            } else {
                layer.msg('测试结果：失败')
            }
            refresh_result(response['data']['result_list']);
        }, function (response) {
            console.log(response);
        })
    })
}
