
function input_filter(elem) {
    if (elem.type == 'hidden')
        return false;
    if (elem.value == '')
        return false;
    return true;
}

var inputs = [].slice.apply(document.getElementsByTagName('input')).filter(input_filter);
inputs = inputs.map(function(element) {
    return { path :  path(element), value : element.value, name : element.name };
});

// wysyłanie wiadomości
var message = "I" + JSON.stringify(inputs)
chrome.extension.sendRequest(message);

function path(elem) {
    var result = [];
    while (elem.parentElement != null) {
        var index = [].indexOf.call(elem.parentElement.children, elem);
        result.push(index);
        elem = elem.parentElement;
    }
    return result;
}


