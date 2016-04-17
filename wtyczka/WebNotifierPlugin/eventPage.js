/**
 * Created by Marek on 2016-04-14.
 */

var stan = "Czy_z_logowaniem"; // Czy_wprowadzone_dane, Czekanie_na_zalogowanie, Dodawanie_obiektów
var inputs = [];
var submit = [];
var objects = [];
var login_url = "";

/* Funkcje akcji dla każdego przycisku */
function Czy_z_logowaniem_tak() {
    stan = "Czy_wprowadzone_dane";
}

function Czy_z_logowaniem_nie() {
    stan = "Dodawanie_obiektów";
}

function Wprowadzone_dane(){
    chrome.tabs.executeScript(null, {file: 'download_inputs.js'});
    stan = "Czekanie_na_zalogowanie";
    chrome.tabs.executeScript(null, {file: 'download_submit.js'});
}

function Zalogowano() {
    stan = "Dodawanie_obiektów";
}

function Dodaj_objekt() {
    chrome.tabs.executeScript(null, {file: 'download_object.js'});
}


function Zapisz_wszystko() {
    chrome.tabs.getSelected(null, function(tab) {
        chrome.tabs.remove(tab.id);
    })

    var url = "data:text/html;charset=utf8,";
    function append(key, value) {
        var input = document.createElement('textarea');
        input.setAttribute('name', key);
        input.textContent = value;
        form.appendChild(input);
    }
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = 'http://127.0.0.1:8000/add/';
    append('login_data',JSON.stringify({ inputs: inputs, submit : submit }));
    append('data_to_observer',JSON.stringify(objects));
    append('url_login', url_login);
    url += encodeURIComponent(form.outerHTML);
    url += encodeURIComponent('<script>document.forms[0].submit();</script>');
    chrome.tabs.create({url: url, active: true});

    stan = "Czy_z_logowaniem";
    inputs = [];
    submit = [];
    objects = [];
    url_login = "";
}


function ObsłuzKlikniecie(przycisk) {
    if (przycisk == "wyswietlanie") ;
    else if (przycisk == "Czy_z_logowaniem_tak") Czy_z_logowaniem_tak();
    else if (przycisk == "Czy_z_logowaniem_nie") Czy_z_logowaniem_nie();
    else if (przycisk == "Wprowadzone_dane") Wprowadzone_dane();
    else if (przycisk == "Dodaj_objekt") Dodaj_objekt();
    else if (przycisk == "Zapisz_wszystko") Zapisz_wszystko();
}

// obsługa popup'a :
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
       ObsłuzKlikniecie(request.dane);
      sendResponse({odp: stan});
  });

// obsługa komunikacji z skryptami:
chrome.extension.onRequest.addListener(function(mess) {
    if (mess[0] == "I") {
        inputs = JSON.parse(mess.substring(1, mess.length));
    }
    else if (mess[0] == "S") {
        if (stan == "Czekanie_na_zalogowanie") {
            submit =  JSON.parse(mess.substring(1, mess.length)).path;
            url_login = JSON.parse(mess.substring(1, mess.length)).url;
            Zalogowano();
        }
    }
    else if (mess[0] == "O") {
        if (stan == "Dodawanie_obiektów") {
            objects.push(JSON.parse(mess.substring(1, mess.length)));
        }
    }
});
