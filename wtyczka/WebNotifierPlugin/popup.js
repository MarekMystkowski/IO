
var view = "";

function update() {
    document.getElementById("login_ask").style.display = "none";
    document.getElementById("login_wait").style.display = "none";
    document.getElementById("objects").style.display = "none";
    document.getElementById(view).style.display = "block";
}

function click(msg) {
    return function() {
        chrome.runtime.sendMessage({data: msg}, function(response) {
            view = response.data;
            update();
        });
    };
}

window.onload = function() {
    document.getElementById("login_yes").addEventListener("click", click("login_yes"));
    document.getElementById("login_no").addEventListener("click", click("login_no"));
    document.getElementById("cancel_login").addEventListener("click", click("cancel"));
    document.getElementById("cancel_objects").addEventListener("click", click("cancel"));
    document.getElementById("save").addEventListener("click", click("save"));
    click("load")();
};
