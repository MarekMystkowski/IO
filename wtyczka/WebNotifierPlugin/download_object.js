
document.addEventListener("click", function(elem) {
    chrome.extension.sendRequest("O" + JSON.stringify({ path: path(elem.target), url: document.URL }));
});

function path(elem) {
    var result = [];
    while (elem.parentElement != null) {
        var index = [].indexOf.call(elem.parentElement.children, elem);
        result.push(index);
        elem = elem.parentElement;
    }
    return result;
}