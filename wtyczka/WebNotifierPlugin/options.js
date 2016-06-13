
var registrationId = "";
var senderId = "699809079851";

function register() {
    chrome.gcm.register([senderId], registerCallback);
}

function registerCallback(regId) {
    registrationId = regId;

    if (chrome.runtime.lastError) {
        chrome.extension.getBackgroundPage().console.log(chrome.runtime.lastError.message);
        alert("Error: error.");
        return;
    }

    chrome.storage.local.set({rid: registrationId});
}

window.onload = function() {
    chrome.storage.local.get("rid", function (result) {
        if (typeof result.rid == "undefined")
        {
            registrationId = "";
            register();
        }
        else
        {
            registrationId = result.rid;
        }
    });
    document.getElementById("connect").addEventListener("click", function(){
        nurl = "http://127.0.0.1:8000/notify_me/?rid=" + registrationId;
        chrome.tabs.create({ url: nurl });
    });
};
