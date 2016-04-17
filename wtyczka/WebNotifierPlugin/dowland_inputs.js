
function filtre_input(elem) {
    if(elem.type == 'hidden')
        return false;
    if(elem.value == '')
        return false;
    return true;
}

var inputs = [].slice.apply(document.getElementsByTagName('input')).filter(filtre_input);
inputs = inputs.map(function(element) {
    return { path :  path(element), value : element.value, name : element.name };
});

// Wysyłąnie wiadomości
var mess = "I" + JSON.stringify(inputs)
chrome.extension.sendRequest(mess);


function path(elem) {
    var result = [];
    while (elem.parentElement != null) {
        chi = elem.parentElement.children;
        var i = 0;
        for (i = 0; i < chi.length; i++) {
            if (chi[i] == elem) {
                result.push(i);
                break;
            }
        }
        elem = elem.parentElement;
    }
    return result;
}


