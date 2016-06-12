
// filtruje pola do wysłania na serwer
function filter(input) {
    if (input.type == 'hidden' || input.type == 'submit')
        return false;
    if (input.value == '')
        return false;
    return true;
}

// zamienia ścieżką względną na bezwzględną
// chyba niepotrzebne, bo form.action jakoś samo się zamienia
function absolute(url, path) {
    if (path.length == 0)
        return url;
    if (path[0] == '/')
        return url.match(/^.+?[^\/]\//)+path.substr(1, path.length-1);
    var stack = url.split('/'), parts = path.split('/');
    stack.pop();
    for (var i = 0; i < parts.length; i++) {
        if (parts[i] == '.')
            continue;
        if (parts[i] == '..')
            stack.pop();
        else
            stack.push(parts[i]);
    }
    return stack.join('/');
}

// przechwycenie logowania
function onSubmit(event) {
    var form = event.target;
    inputs = [].slice.apply(form.getElementsByTagName('input')).filter(filter);
    var input_data = {};
    inputs.forEach(function (input) {
        input_data[input.name] = input.value;
    });
    chrome.runtime.sendMessage({
        type: "login",
        login_url: {get: document.URL, post: form.action},
        login_data: input_data
    });
}
[].forEach.call(document.getElementsByTagName('form'), function (form) {
    form.addEventListener('submit', onSubmit);
});

// wiadomość ze skryptu tła
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    // zatrzymaj funkcję przechwytującą logowanie
    if (request.message == "stop_login") {
        [].forEach.call(document.getElementsByTagName('form'), function (form) {
            form.removeEventListener("submit", onSubmit);
        });
    }
});
