String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};
function addslashes( str ) {
    return str.replaceAll("\\", "\\\\").replaceAll("'", "\\'");
}


document.addEventListener("click", function(elem) {
    chrome.extension.sendRequest("O{ 'path' : " + path(elem.target) +
        " , 'url' : '" + addslashes(document.URL) + "' }");
});


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
