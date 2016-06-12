
// pobiera ścieżkę elementu
function getPath(elem) {
    var result = [];
    while (elem.parentElement != null) {
        if (elem.id) {
            // jeśli element ma id, dodajemy je do ścieżki i kończymy
            result.push(elem.id);
            break;
        }
        var index = [].indexOf.call(elem.parentElement.children, elem);
        result.push(index);
        elem = elem.parentElement;
    }
    return result.reverse();
}

// znajduje element o danej ścieżce
function getElement(path) {
    var e = document.documentElement;
    path.forEach(function(index) {
        e = e.children[index];
    });
    return e;
}

// pozycja myszy
var mouseX, mouseY;
document.addEventListener("mousemove", function(event) {
    mouseX = event.clientX;
    mouseY = event.clientY;
});

// tworzy nowy div służący do oznaczania elementów
function addHighlight(color) {
    var div = document.createElement('div');
    div.className = 'web-notifier-highlight';
    div.style.zIndex = 2000000000;
    div.style.backgroundColor = "rgba(" + color.r + ", " + color.g + ", " + color.b + ", " + color.a + ")";
    div.style.outline = "2px solid rgba(" + Math.round(color.r*0.5) + ", " + Math.round(color.g*0.5) + ", " + Math.round(color.b*0.5) + ", " + color.a + ")";
    document.body.appendChild(div);
    return div;
}

// ustawia div nad elementem do zaznaczenia
function setHighlightPosition(div, element, position) {
    var rect = element.getBoundingClientRect();
    div.style.display = "block";
    div.style.position = position;
    div.style.left = rect.left+"px";
    if (position == "fixed")
        div.style.top = rect.top+"px";
    else if (position == "absolute") {
        doc = document.documentElement;
        div.style.top = (rect.top + (window.pageYOffset || doc.scrollTop) - (doc.clientTop || 0))+"px";
    }
    div.style.width = (rect.right-rect.left)+"px";
    div.style.height = (rect.bottom-rect.top)+"px";
}

// dodawanie i usuwanie obiektów
function highlightElement(element) {
    var div = addHighlight({ r: 83, g: 182, b: 136, a: 0.4 });
    setHighlightPosition(div, element, "absolute");
}
function onKeyDown(event) {
    var element = document.elementFromPoint(mouseX, mouseY);
    if (element === null)
        return;

    if ((event.keyCode == 107 || event.keyCode == 187) && element.className != "web-notifier-highlight") { // klawisz +
        chrome.runtime.sendMessage({
            type: "add_object",
            page_url: document.URL,
            page_title: document.title,
            object_path: getPath(element)}
        );
        highlightElement(element);

    } else if ((event.keyCode == 109 || event.keyCode == 189) && element.className == "web-notifier-highlight") { // klawisz -
        element.parentElement.removeChild(element);
        chrome.runtime.sendMessage({
            type: "remove_object",
            page_url: document.URL,
            object_path: getPath(element)}
        );
    }
}
document.addEventListener("keydown", onKeyDown);


// div wyświetlany nad elementem wskazywanym myszką
var highlightDiv = addHighlight({ r: 56, g: 114, b: 189, a: 0.4 });
highlightDiv.style.pointerEvents = "none"; // żeby nie przykrywał innych elementów

// odświeżanie pozycji diva co 16ms
var timer = window.setInterval(function() {
    var element = document.elementFromPoint(mouseX, mouseY);
    if (element === null)
        return;
    setHighlightPosition(highlightDiv, element, "fixed");
}, 16);


// wiadomość ze skryptu tła
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

    if (request.message == "add_objects") {
        // zaznacz obiekty, które zostały dodane wcześniej na tej stronie
        request.data.forEach(function(path) {
            highlightElement(getElement(path));
        });

    } else if (request.message == "stop_objects") {
        // zatrzymaj zaznaczanie obiektów
        clearInterval(timer);
        document.removeEventListener("keydown", onKeyDown);
        var divs = [].slice.apply(document.getElementsByClassName("web-notifier-highlight"));
        divs.forEach(function(div) {
            div.parentElement.removeChild(div);
        });
    }
});
