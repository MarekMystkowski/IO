String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};

var inputs = [].slice.apply(document.getElementsByTagName('input'));
inputs = inputs.map(function(element) {
    return "{ 'path' : " + path(element) + " , 'value' : '" + addslashes(element.value) + "'  }";
});

// Sklejenie w jeden napis.
var mess = "I[ { 'url' : '" + addslashes(document.URL) + "' }" ;
for (var index in inputs) mess += ' , ' + inputs[index];
mess += ' ]';

chrome.extension.sendRequest(mess);



function path(elem) {
    var result = "";
    var par;
    while (elem.parentElement != null) {
        par = elem.parentElement;
        chi = par.children;
        var i = 0;
        for (i = 0; i < chi.length; i++) {
            if (chi[i] == elem) result = i + ", " + result;
        }
        elem = par;
    }
    if (result.length > 0) result = result.substring(0, result.length - 2);
    return result = "( " + result + " )";
}

function addslashes( str ) {
    return str.replaceAll("\\", "\\\\").replaceAll("'", "\\'");
}
