
var co_klikniete = "";
var jaki_widok = "";
function PoinformujOKliknieciu() {
    chrome.runtime.sendMessage({dane: co_klikniete}, function(response) {
        jaki_widok = response.odp;
        PoprawHTML();
    });
}

window.onload = function() {
    chrome.runtime.sendMessage({dane: "wyswietlanie"}, function(response) {
        jaki_widok = response.odp;
        PoprawHTML();
    });
};

function PoprawHTML() {
    var ukryty = "display:none";
    var widoczny = "";
    document.getElementById("Czy_z_logowaniem").style = ukryty;
    document.getElementById("Czy_wprowadzone_dane").style = ukryty;
    document.getElementById("Czekanie_na_zalogowanie").style = ukryty;
    document.getElementById("Dodawanie_obiektów").style = ukryty;
    document.getElementById(jaki_widok).style = widoczny;
}

function klikniecie(co) {
    return function () {
        co_klikniete = co;
        PoinformujOKliknieciu();
    };
}

document.getElementById("tak").addEventListener("click", klikniecie("Czy_z_logowaniem_tak"));
document.getElementById("nie").addEventListener("click", klikniecie("Czy_z_logowaniem_nie"));
document.getElementById("wprowadzone").addEventListener("click", klikniecie("Wprowadzone_dane"));
document.getElementById("dodaj").addEventListener("click", klikniecie("Dodaj_objekt"));
document.getElementById("zapisz").addEventListener("click", klikniecie("Zapisz_wszystko"));
