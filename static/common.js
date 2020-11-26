function http(url, method, data, success, error) {
    data = method === 'get' ? data : JSON.stringify(data);
    $.ajax({
        url: url,
        type: method,
        contentType: 'application/json;charset=UTF-8',
        dataType: 'json',
        data: data,
        success: success,
        error: error
    })
}

function update_user() {
    http('/user', 'post', {}, function (response) {
        $('#user').text(response['username'])
    }, function (response) {
        console.log(response)
    })
}