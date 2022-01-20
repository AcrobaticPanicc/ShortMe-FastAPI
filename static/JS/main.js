function submitPassowrd(url) {
    let password = document.getElementById('password').value;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:8080');
    xhr.send(JSON.stringify({password: password}));
    let u = xhr.responseText
    let ur = decodeURI(u)


    if (xhr.status === 200) {
        window.location = ur;
        return false
    }
    window.location.replace(u);
    return false
}