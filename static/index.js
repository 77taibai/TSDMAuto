function closeCAA(){
    $('#mainCAA').hide()
    $('#mcaaid').val('')
    $('#mcaaname').val('')
    $('#mcaacookie').val('')
}

function mainCAAU(){
    let id = $('#mcaaid').val()
    let name = $('#mcaaname').val()
    let cookie = $('#mcaacookie').val()
    let pwd = localStorage.getItem('pwd')
    if (pwd === null){
        window.location.href = '/login'
    }
    $.post('/api/user/add', {'pwd': pwd, 'id': id, 'cookie': cookie, 'name': name}, function (e){
        if (e['code'] === '0000'){
            alert('添加成功！')
            closeCAA()
        }else if (e['code'] === '0101'){
            alert('已存在')
            closeCAA()
        }else {
            alert('不知道')
            closeCAA()
        }
        loadUser()
    })
}

function loadUser(){
    $('#mainCTable').children().remove()
    let pwd = localStorage.getItem('pwd')
    if (pwd === null){
        window.location.href = '/login'
    }
    $.post('/api/user/all', {'pwd': pwd}, function (e){
        for (let eKey in e) {
            $('#mainCTable').append(`<tr>
                <td>${e[eKey][0]}</td>
                <td>${e[eKey][1]}</td>
                <td>${e[eKey][2]}</td>
                <td onclick="delUser('${e[eKey][0]}')">❌</td>
            </tr>`)
        }
    })
}

function delUser(id){
    let pwd = localStorage.getItem('pwd')
    if (pwd === null){
        window.location.href = '/login'
    }
    $.post('/api/user/del', {'pwd': pwd, 'id': id}, function (){
        loadUser()
    })
}

function openC(){
    $('#mainC').show()
    $('#mainS').hide()
    loadUser()
}

function openS(){
    $('#mainC').hide()
    $('#mainS').show()
}

window.onload = function (){
    let pwd = localStorage.getItem('pwd')
    if (pwd === null){
        window.location.href = '/login'
    }

    $.post('/api/tsb', {'pwd': pwd}, function (e){
        $("#mainStatusH").text('天使币：' + e)
    })
    $.post('/api/status', {'pwd': pwd}, function (e){
        let qd
        let a = (e['msg']['qd'] / 1000000 + 86460000) >= new Date().getTime()
        let b = (e['msg']['dg'] / 1000000 + 21780000) >= new Date().getTime()
        if (a === true && b === true){
            $('#mainStatusTop').text('一切正常')
        }else if (a === true && b === false){
            $('#mainStatusTop').text('打工异常！')
        }else if (a === false && b === true){
            $('#mainStatusTop').text('签到异常！')
        } else {
            $('#mainStatusTop').text('系统崩溃')
        }
    })
}

function loaddg(){
    $('#mainStatusLogQDB').hide()
    $('#mainStatusLogDGB').show().children().remove()
    let pwd = localStorage.getItem('pwd')
    if (pwd === null){
        window.location.href = '/login'
    }
    $.post('/api/log/dg', {'pwd': pwd}, function (e){
        for (let eKey in e) {
            $('#mainStatusLogDGB').append(`<tr><td>${timeFormat(e[eKey][0] / 1000000)}</td><td>${e[eKey][1]}</td></tr>`)
        }
    })
}

function loadqd(){
    $('#mainStatusLogQDB').show().children().remove()
    $('#mainStatusLogDGB').hide()
    let pwd = localStorage.getItem('pwd')
    if (pwd === null){
        window.location.href = '/login'
    }
    $.post('/api/log/qd', {'pwd': pwd}, function (e){
        for (let eKey in e) {
            $('#mainStatusLogQDB').append(`<tr><td>${timeFormat(e[eKey][0] / 1000000)}</td><td>${e[eKey][1]}</td></tr>`)
        }
    })
}



function timeFormat(time){
    time = parseInt(time)
    if (time === 0){
        return '没有进行过'
    }
    //datetime是拿到的时间戳
    let date = new Date(time);//时间戳为10位需*1000，时间戳为13位的话不需乘1000
    let year = date.getFullYear(),
    month = ("0" + (date.getMonth() + 1)).slice(-2),
    sdate = ("0" + date.getDate()).slice(-2),
    hour = ("0" + date.getHours()).slice(-2),
    minute = ("0" + date.getMinutes()).slice(-2),
    second = ("0" + date.getSeconds()).slice(-2);
    // 拼接 返回
    return year + "-" + month + "-" + sdate + " " + hour + ":" + minute + ":" + second;
}
