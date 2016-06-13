
var state = "login_ask"; // login_ask, login_wait, objects
var page_data = {};
var login_url = {};
var login_data = {};


// funkcja wołana po executeScript
function callback() {
    if (chrome.runtime.lastError) {
        chrome.extension.getBackgroundPage().console.log(chrome.runtime.lastError.message);
    } else {
        // Tab exists
    }
}

/* Funkcje akcji */

function action_login_yes() {
    state = "login_wait";
    // czekaj na zalogowanie na dowolnej karcie
    chrome.tabs.query({}, function(tabs) {
        tabs.forEach(function(tab) {
            chrome.tabs.executeScript(tab.id, {file: "login.js"}, callback);
        })
    });
}

function action_login_no() {
    action_objects();
}

function action_objects(){
    state = "objects";
    // zatrzymaj skrypt przechwytujący logowanie
    // i uruchom zaznaczanie obiektów na wszystkich otwartych kartach
    chrome.tabs.query({}, function(tabs) {
        tabs.forEach(function(tab) {
            chrome.tabs.sendMessage(tab.id, {message: "stop_login"});
            chrome.tabs.executeScript(tab.id, {file: "objects.js"}, callback);
        })
    });
}

function action_stop() {
    // zatrzymaj skrypty
    chrome.tabs.query({}, function(tabs) {
        tabs.forEach(function(tab) {
            chrome.tabs.sendMessage(tab.id, {message: "stop_login"});
            chrome.tabs.sendMessage(tab.id, {message: "stop_objects"});
        })
    });
    state = "login_ask";
    page_data = {};
    login_url = {};
    login_data = {};
}

function action_save() {
    // czy zostały wybrane jakiekolwiek elementy?
    var page_url = "";
    for (var key in page_data)
        if (page_data.hasOwnProperty(key))
            page_url = key;
    if (page_url.length == 0)
        return;

    // prześlij dane na serwer
    var url = "data:text/html;charset=utf8,";
    function append(key, value) {
        var input = document.createElement('textarea');
        input.setAttribute('name', key);
        input.textContent = value;
        form.appendChild(input);
    }
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = 'http://127.0.0.1:8000/add_page/';
    append('page_url', page_url);
    append('page_title', page_data[page_url].title);
    append('page_data', JSON.stringify(page_data[page_url].paths));
    append('login_url', JSON.stringify(login_url));
    append('login_data', JSON.stringify(login_data));
    url += encodeURIComponent(form.outerHTML);
    url += encodeURIComponent('<script>document.forms[0].submit();</script>');
    chrome.tabs.create({url: url, active: true});

    action_stop();
}


/* Zdarzenia */



// otwarcie nowej strony na karcie
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (changeInfo.status == "complete") {
        if (state == "login_wait") {
            // wywołaj skrypt przechwytujący logowanie
            chrome.tabs.executeScript(tabId, {file: "login.js"}, callback);
        } else if (state == "objects") {
            // wywołaj skrypt do wybierania obiektów
            chrome.tabs.executeScript(tabId, {file: "objects.js"}, callback);
            // wyślij do niego wiadomość z wybranymi wcześniej elementami
            setTimeout(function() {
                if (tab.url in page_data)
                    chrome.tabs.sendMessage(tabId, { message: "add_objects", data: page_data[tab.url].paths });
            }, 50);
        }
    }
});


/* Przesyłanie wiadomości */

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

    // obsługa skryptów
    if (request.type == "login") {
        login_url = request.login_url;
        login_data = request.login_data;
        action_objects();
    }
    else if (request.type == "add_object") {
        // na razie możemy dodawać tylko jedną stronę
        if (Object.keys(page_data).length == 0 || request.page_url in page_data) {
            if (!(request.page_url in page_data))
            {
                page_data[request.page_url] = {};
                page_data[request.page_url].paths = [];
            }
            page_data[request.page_url].title = request.page_title;
            page_data[request.page_url].paths.push(request.object_path);
        }
    }
    else if (request.type == "remove_object") {
        var arr = page_data[request.page_url].paths;
        var index = arr.indexOf(request.object_path);
        arr.splice(index, 1);
        if (arr.length == 0)
            delete page_data[request.page_url].paths;
    }

    // obsługa popup'a
    else if (request.data == "load");
    else if (request.data == "login_yes")
        action_login_yes();
    else if (request.data == "login_no")
        action_login_no();
    else if (request.data == "cancel")
        action_stop();
    else if (request.data == "save")
        action_save();
    sendResponse({data: state});
});

chrome.runtime.onInstalled.addListener(function(details){
     chrome.runtime.openOptionsPage();
});

// Powiadomienia

// curl to testowania
// curl -H "Content-Type:application/x-www-form-urlencoded;charset=UTF-8" -H "Authorization: key= AIzaSyAezekme7gnKSMaZht4mRlPQLRZWU3hXs8" -d "registration_id=APA91bFLNtkQT4WeKdINpweqLtqV_cu3CuZEIOJgY8B4f88RzMHOuZTpCd_vJSlIM4JqJqAbVYuWnnH6kyK8LIpmy58pPL72_kW5YAhKxWUeE5fVEeQHgfE8PKQMqw1ZfR3YNHuGmUFNbyk3nz7j4nNBtFcHb2SUBQ" -d data.YOUR_MESSAGE_KEY=YOUR_MESSAGE_VALUE https://android.googleapis.com/gcm/send

function getNotificationId() {
  var id = Math.floor(Math.random() * 9007199254740992) + 1;
  return id.toString();
}

function messageReceived(message) {

  var messageString = "";
  // for (var key in message.data) {
  //   if (messageString != "")
  //     messageString += ", "
  //   messageString += key + ":" + message.data[key];
  // }
  messageString += message.data['message'];

  chrome.notifications.create(getNotificationId(), {
    title: "Nowa zmiana",
    iconUrl: 'icon.png',
    type: "basic",
    message: messageString
  }, function() {});
}

chrome.gcm.onMessage.addListener(messageReceived);
