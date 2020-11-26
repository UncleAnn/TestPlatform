function init_team(form) {
    // 加载团队team
    let url = '/variable/api/v1/aggregate';
    let data = {
        // type指数据库集合
        type: 'team',
        key: 'team'
    };
    http(url, 'post', data, function (response) {
        console.log(response);
        // option动态拼接
        // 先拼接team
        let teamData = response['data'];
        let html = '';
        for (index in teamData) {
            let value = teamData[index]['_id'];
            html += `<option value="${value}">${value}</option>`;
        }
        $('#teamInput').append(html);
        // 再拼接project
        let team;
        for (index in teamData) {
            team = teamData[index]['_id'];
            // 循环只执行一次，获取第一个team值，便于加载页面时的默认project拼接
            break;
        }
        let url = '/variable/api/v1/searchProject';
        let data = {
            "type": 'team',
            "team": team
        };
        http(url, 'post', data, function (response) {
            console.log(response);
            let projectData = response['data'];
            let html = '';
            for (index in projectData) {
                let value = projectData[index]['project'];
                html += `<option value="${value}">${value}</option>`;
            }
            $('#projectInput').append(html);
            // 表单html改变需要手动render
            form.render();
        }, function (response) {
            console.log(response);
        })
    })
}

$(function () {
    init_team();
})