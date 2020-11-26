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

function addHeaderLine() {
    $('#headerBtn').click(function () {
        let html = "";
        html += '<div class="layui-form-item headerLine">' +
            // '<div class="layui-input-inline">' +
            '<div class="layui-inline">' +
            '<input type="text" class="layui-input headerKey" lay-verify="required" placeholder="请输入header键">' +
            '</div>' +
            // '<div class="layui-input-inline">' +
            '<div class="layui-inline">' +
            '<input type="text" class="layui-input headerValue" lay-verify="required" placeholder="请输入header值">' +
            '</div>' +
            '<div class="layui-inline">' +
            '<input type="button" class="headerDel layui-btn layui-btn-danger" value="delete">' +
            '</div>' +
            '</div>';
        let section = $('#header');
        section.append(html);
        section.show();
    })
}

function delHeaderLine() {
    let dom = $('#header');
    dom.on('click', '.headerDel', function () {
        let i = $('.headerDel').index($(this));
        $('.headerLine').eq(i).remove();
    });
}

function loadHeaderInfo(load_data) {
    // 将value一次性拼到html里
    if (load_data.hasOwnProperty('header')) {
        let section = $('#header');
        let headerInfo = load_data['header'];
        let html = "";
        for (key in headerInfo) {
            let value = headerInfo[key];
            html += '<div class="layui-form-item">' +
                '<div class="layui-input-inline">' +
                '<input type="text" class="layui-input headerKey" lay-verify="required" ' +
                `value="${key}" placeholder="请输入header键">` +
                '</div>' +
                '<div class="layui-input-inline">' +
                '<input type="text" class="layui-input headerValue" lay-verify="required" ' +
                `value="${value}" placeholder="请输入header值">` +
                '</div>' +
                '</div>';
        }
        section.append(html);
        section.show();
    }
}

function loadParamsInfo(load_data) {
    let html = "";
    for (key in load_data['params']) {
        let value = load_data['params'][key];
        html += '<div class="layui-form-item">' +
            '<div class="layui-input-inline">' +
            '<input type="text" class="layui-input paramKey" lay-verify="required" ' +
            `value="${key}" placeholder="请输入params键">` +
            '</div>' +
            '<div class="layui-input-inline">' +
            '<input type="text" class="layui-input paramValue" lay-verify="required" ' +
            `value="${value}" placeholder="请输入params值">` +
            '</div>' +
            '</div>';
    }
    let section = $('#params');
    section.append(html);
    section.show();
}

function addParamsLine() {
    $('#paramsBtn').click(function () {
        let html = "";
        html += '<div class="layui-form-item param-line">' +
            '<div class="layui-inline">' +
            '<input type="text" class="layui-input paramKey" lay-verify="required" placeholder="请输入params键">' +
            '</div>' +
            '<div class="layui-inline">' +
            '<input type="text" class="layui-input paramValue" lay-verify="required" placeholder="请输入params值">' +
            '</div>' +
            '<div class="layui-inline">' +
            '<input type="button" class="layui-btn layui-btn-danger param-del" value="delete">' +
            '</div>' +
            '</div>';
        let section = $('#params');
        section.append(html);
        section.show();
    });
}

function delParamsLine() {
    let dom = $('#params');
    dom.on('click', '.param-del', function () {
        let i = $('.param-del').index($(this));
        $('.param-line').eq(i).remove();
    })
}

function loadAssertInfo(load_data) {
    if (load_data.hasOwnProperty('assert')) {
        let assertInfo = load_data['assert'];
        let html = "";
        // 动态拼接页面
        for (let i = 0; i < assertInfo.length; i++) {
            html += '<div class="layui-form-item">' +
                '<div class="layui-block">' +
                '<div class="layui-input-inline">' +
                '<select name="assertType" lay-verify="required" class="assertType">' +
                '<option value="statusCode">状态码</option>' +
                '<option value="body">响应体</option>' +
                '</select>' +
                '</div>' +
                '<div class="layui-input-inline">' +
                '<input type="text" class="layui-input assertExpr" required lay-verify="required" ' +
                'placeholder="请输入断言表达式" id="assertExp">' +
                '</div>' +
                '<div class="layui-input-inline">' +
                '<select name="assertCondition" class="assertCondition" lay-verify="required"> ' +
                '<option value="equal" selected>==</option>' +
                '<option value="greater_equal">>=</option>' +
                '<option value="lower_equal"><=</option>' +
                '<option value="greater">></option>' +
                '<option value="lower"><</option>' +
                '<option value="include">包含</option>' +
                '</select>' +
                '</div>' +
                '<div class="layui-input-inline">' +
                '<input type="text" class="layui-input assertValue" lay-verify="required" ' +
                'placeholder="请输入预期值">' +
                '</div>' +
                '</div>' +
                '</div>';
        }
        let section = $('#assert');
        section.append(html);
        // TODO 定位不到元素
        let dom = $('.assertType');
        // 循环加载断言信息
        dom.each(function (index, element) {
            let info = assertInfo[index];
            let type = info['assertType'];
            // 原生js赋值使用=
            element.value = type;
            if (type === 'body') { // 断言状态码时，填表达式和比较符
                $('.assertExpr').eq(index).val(info['assertExpr']);
                $('.assertCondition').eq(index).val(info['assertCondition']);
            } else { // 断言状态码时，不填表达式，比较符只能是等于
                $('.assertCondition').eq(index).val('equal');
            }
            // 填预期值
            $('.assertValue').eq(index).val(info['assertValue']);
        });
        section.show();
    }
}

function addAssertLine(form) {
    $('#assertBtn').click(function () {
        let html = "";
        html += '<div class="layui-form-item assert-line">' +
            '<div class="layui-block">' +
            '<div class="layui-input-inline">' +
            '<select name="assertType" lay-verify="required" class="assertType">' +
            '<option value="statusCode">状态码</option>' +
            '<option value="body" selected>响应体</option>' +
            '</select>' +
            '</div>' +
            '<div class="layui-input-inline">' +
            '<input type="text" class="layui-input assertExpr" required lay-verify="required"' +
            'placeholder="请输入断言表达式" id="assertExp">' +
            '</div>' +
            '<div class="layui-input-inline">' +
            '<select name="assertCondition" class="assertCondition" lay-verify="required">' +
            '<option value="equal" selected>==</option>' +
            '<option value="greater_equal">>=</option>' +
            '<option value="lower_equal"><=</option>' +
            '<option value="greater">></option>' +
            '<option value="lower"><</option>' +
            '<option value="include">包含</option>' +
            '</select>' +
            '</div>' +
            '<div class="layui-input-inline">' +
            '<input type="text" class="layui-input assertValue" lay-verify="required"' +
            'placeholder="请输入预期值">' +
            '</div>' +
            '<div class="layui-inline">' +
            '<input type="button" class="layui-btn layui-btn-danger assert-del" value="delete">' +
            '</div>' +
            '</div>' +
            '</div>';
        let section = $('#assert');
        section.append(html);
        section.show();
        // layui的机制决定了拼接下拉框之后form必须重新render一次
        form.render();
    });
}

function delAssertLine() {
    let dom = $('#assert');
    dom.on('click', '.assert-del', function () {
        let i = $('.assert-del').index($(this));
        $('.assert-line').eq(i).remove();
    })
}

function loadExtractInfo(load_data) {
    if (load_data.hasOwnProperty('extract')) {
        let extractInfo = load_data['extract'];
        let section = $('#extract');
        let html = "";
        for (let i = 0; i < extractInfo.length; i++) {
            html += '<div class="layui-form-item">' +
                '<div class="layui-input-inline">' +
                '<input type="text" class="layui-input extractExpr" lay-verify="required" placeholder="提取表达式">' +
                '</div>' +
                '<div class="layui-input-inline">' +
                '<input type="text" class="layui-input extractValue" lay-verify="required" placeholder="提取变量名">' +
                '</div>' +
                '</div>';
        }
        section.append(html);
        $('.extractExpr').each(function (index, element) {
            let info = extractInfo[index];
            element.value = info['extractExpr'];
            $('.extractValue').val(info['extractValue']);
        });
        section.show();
    }
}

function getExtractInfo() {
    let extract = [];
    let dom = $('.extractExpr');
    dom.each(function (index, element) {
        let expr = element.value;
        if (expr !== '') {
            extract.push({
                extractExpr: expr,
                extractValue: $('.extractValue').eq(index).val(),
            })
        }
    });
    return extract;
}

function getAssertInfo() {
    let assert = [];
    let dom = $('.assertType');
    dom.each(function (index, element) {
        let type = element.value;
        let expr = $('.assertExpr').eq(index).val();
        if (type === 'statusCode') {
            assert.push({
                assertType: type,
                // assertCondition: $('.assertCondition').eq(index).val(),
                assertValue: $('.assertValue').eq(index).val()
            });
        } else if (expr !== '') {
            assert.push({
                assertType: type,
                assertExpr: expr,
                assertCondition: $('.assertCondition').eq(index).val(),
                assertValue: $('.assertValue').eq(index).val()
            });
        }
    });
    return assert;
}

function addExtractLine() {
    $('#extractBtn').click(function () {
        let html = "";
        html += '<div class="layui-form-item extract-line">' +
            '<div class="layui-input-inline">' +
            '<input type="text" class="layui-input extractExpr" lay-verify="required" placeholder="提取表达式">' +
            '</div>' +
            '<div class="layui-input-inline">' +
            '<input type="text" class="layui-input extractValue" lay-verify="required" placeholder="提取变量名">' +
            '</div>' +
            '<div class="layui-inline">' +
            '<input type="button" class="layui-btn layui-btn-danger extract-del" value="delete">' +
            '</div>' +
            '</div>';
        let section = $('#extract');
        section.append(html);
        section.show();
    });
}

function delExtractLine() {
    let dom = $('#extract');
    dom.on('click', '.extract-del', function () {
        let i = $('.extract-del').index($(this));
        $('.extract-line').eq(i).remove();
    })
}
function getHeaderInfo() {
    let header = {};
    let dom = $('.headerKey');
    dom.each(function (index, element) {
        let key = element.value;
        // let key = dom.eq(index).val();
        if (key !== '') {
            header[key] = $('.headerValue').eq(index).val();
        }
    });
    return header;
}

function getParamsInfo() {
    let params = {};
    let dom = $('.paramKey');
    dom.each(function (index, element) {
        let key = element.value;
        if (key !== '') {
            params[key] = $('.paramValue').eq(index).val();
        }
    });
    return params;
}

function getData() {
    let data = {
        method: $('#method').val(),
        team: $('#team').val(),
        project: $('#project').val(),
    };
    //判断是新增接口还是修改接口
    let path = window.location.pathname;
    let pathList = path.split('/');
    if ($.inArray('edit', pathList) !== -1) {
        data['_id'] = pathList[pathList.length - 1]
    }
    //获取接口描述信息
    let descInfo = $('#description').val();
    if (descInfo !== '') {
        data['description'] = descInfo
    }
    //获取header信息
    let headerInfo = getHeaderInfo();
    if (Object.keys(headerInfo).length > 0) {
        data['header'] = headerInfo;
    }
    //获取params信息
    let paramsInfo = getParamsInfo();
    if (Object.keys(paramsInfo).length > 0) {
        data['params'] = paramsInfo;
    }
    //获取assert信息
    let assertInfo = getAssertInfo();
    if (Object.keys(paramsInfo).length > 0) {
        data['assert'] = assertInfo;
    }
    //获取extract信息
    let extractInfo = getExtractInfo();
    if (extractInfo.length > 0) {
        data['extract'] = extractInfo;
    }

    console.log(data);
    return data;
}

function debug(layer) {
    $('#debugBtn').click(function () {
        let data = getData(layer);
        data['url'] = $('#url').val();
        // 校验页面url是否已填写
        if (data['url'] === '') {
            layer.msg('请输入url！')
        } else {
            // 信息完成，发起请求
            http('/interface/api/v1/debug', 'post', data, function (response) {
                console.log(response);
                let responseHtml = '<pre><code>' + JSON.stringify(response['data']['response']['data'], null, 4) + '</code></pre>';
                $('#responseText').html(responseHtml);
            }, function (response) {
                console.log(response)
            })
        }
    })
}

function save(layer) {
    $('#saveBtn').click(function () {
        let data = getData(layer);
        data['url'] = $('#url').val();
        // 校验页面url是否已填写
        if (data['url'] === '') {
            layer.msg('请输入url！')
        } else {
            http('/interface/api/v1/save', 'post', data, function (response) {
                console.log(response);
                layer.msg('保存成功')
            }, function (response) {
                console.log(response)
            })
        }
    })
}

function load_interface(case_id, form) {
    // 全局变量
    let load_data;
    // 将接口原内容填充到页面
    http('/interface/api/v1/search', 'post', {'_id': case_id}, function (response) {
        load_data = response['data'][0];
        $('#url').val(load_data['url']);
        $('#method').val(load_data['method']);
        $('#description').val(load_data['description']);
        let team = load_data['team'];
        $('#team').val(team);
        // 根据当前team获取project列表并拼接project option
        http('/variable/api/v1/searchProject', 'post', {"type": 'team', "team": team}, function (response) {
            let dom = $('#project');
            dom.empty();
            let projectData = response['data'];
            let html = '';
            for (index in projectData) {
                let value = projectData[index]['project'];
                html += `<option value="${value}">${value}</option>`;
            }
            dom.append(html);
            form.render();
        }, function (response) {
            console.log(response);
        });
        $('#project').val(load_data['project']);
        // 加载Header信息
        loadHeaderInfo(load_data);
        // 加载Params信息
        loadParamsInfo(load_data);
        // 加载assert信息
        loadAssertInfo(load_data);
        // 加载extract信息
        loadExtractInfo(load_data);
        // layui的机制决定了拼接下拉框之后form必须重新render一次
        form.render();
    }, function (response) {
        console.log(response)
    });
}
