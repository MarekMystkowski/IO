document.addEventListener("click", function(elem) {
    chrome.extension.sendRequest("O" + JSON.stringify({ path : path(elem.target) , url : document.URL }));
});

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