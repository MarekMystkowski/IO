/**
 * Created by Marek on 2016-04-14.
 */

var stan = "Czy_z_logowaniem"; // Czy_wprowadzone_dane, Czekanie_na_zalogowanie, Dodawanie_obiektów
var inputs = "";
var submit = "";
var _objects = "";

/* Funkcje akcji dla każdego przycisku */
function Czy_z_logowaniem_tak() {
    stan = "Czy_wprowadzone_dane";
}

function Czy_z_logowaniem_nie() {
    stan = "Dodawanie_obiektów";
    _objects = "[ ";
}

function Wprowadzone_dane(){
    chrome.tabs.executeScript(null, {file: 'dowland_inputs.js'});
    stan = "Czekanie_na_zalogowanie";
    chrome.tabs.executeScript(null, {file: 'dowland_submit.js'});
}

function Zalogowano() {
    stan = "Dodawanie_obiektów";
    _objects = "[ ";
}

function Dodaj_objekt() {
    chrome.tabs.executeScript(null, {file: 'dowland_object.js'});
}

function Zapisz_wszystko() {
    chrome.tabs.executeScript(null, {file: 'not_dowland.js'});
    if (_objects.length > 2) _objects = _objects.substring(0, _objects.length - 2);
    _objects += " ]";
    var mess_to_server = "{ 'inputs' : " + inputs + " , 'submit' : " + submit +
        " , 'objeects' : " + _objects + " }";

    console.log(mess_to_server);
    // TODO : WYSYLANIR NA SERWER
    

    stan = "Czy_z_logowaniem";
    inputs = "";
    submit = "";
    _objects = "";
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
    if (mess[0] == "I") inputs = mess.substring(1, mess.length);
    if (mess[0] == "S") {
        if (stan == "Czekanie_na_zalogowanie") {
            submit =  mess.substring(1, mess.length);
            Zalogowano();
        }
    }
    if (mess[0] == "O") {
        if (stan == "Dodawanie_obiektów") {
            _objects += mess.substring(1, mess.length) + ", ";
        }
    }
});