
// pobiera ścieżkę elementu
function getPath(elem) {
    var result = [];
    while (elem.parentElement != null) {
        var index = [].indexOf.call(elem.parentElement.children, elem);
        result.push(index);
        elem = elem.parentElement;
    }
    return result.reverse();
}

// filtruje pola do wysłania na serwer
function filter(input) {
    if (input.type == 'hidden' || input.type == 'submit')
        return false;
    if (input.value == '')
        return false;
    return true;
}

// kliknięcie w przycisk submit
function onClick(event) {
    var elem = event.target;
    if (elem.type == "submit") {
        inputs = [].slice.apply(document.getElementsByTagName('input')).filter(filter);
        inputs = inputs.map(function (input) {
            return {name: input.name, value: input.value};
        });
        chrome.runtime.sendMessage({
            type: "login",
            login_url: document.URL,
            login_data: {inputs: inputs, submit: getPath(elem)}
        });
    }
}
document.addEventListener("click", onClick);

// wiadomość ze skryptu tła
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    // zatrzymaj funkcję przechwytującą logowanie
    if (request.message == "stop_login") {
        document.removeEventListener("click", onClick);
    }
});