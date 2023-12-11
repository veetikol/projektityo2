'use strict';

/* 1. show map using Leaflet library. (L comes from the Leaflet library) */

// Haetaan kartta ja keskitetään se aluksi Lontooseen
const map = L.map('map').setView([51.505, -0.09], 13);

// Pinnamerkitsijän lisääminen karttaan
const marker = L.marker([51.5, -0.09]).addTo(map);

// Pop-up toiminnot markkereille, openPopup()-metodi avaa ikkunan välittömästi
marker.bindPopup("I am a marker.").openPopup();

// Popup-ikkuna toiminto karttaan
const popup = L.popup();

// TileLayerin lisääminen (openstreetmapista)
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Metodi, joka palauttaa paikan koordinaatin käyttäjän painaessa karttaa
function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

// Tapahtumakäsittelijä onMapClick -metodille
map.on('click', onMapClick);

// funktio, joka vääntää stringien alkukirjaimet isoksi
function capitalizeFirstLetter(text) {
    return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

// globaalit muuttujat

let pelaajanimi = "";
let playerGuess = "";
let startURL = window.location.href;
let distanceTraveled = 0;
let targetCountry = "";
let GuessedRight = false;
const pelaajaformi = document.getElementById('pelaajainput');
const startnappula = document.querySelector('#startnappula');
const nimilaatikko = document.getElementById('nimi');
const nimiInput = nimilaatikko.querySelector('p');
const emptyname = document.getElementById('emptyname');
const guessButton = document.getElementById('guessButton');
const countriesButton = document.getElementById('countriesButton');
const guessForm = document.getElementById('guessForm');
const guessInput = document.getElementById('guessInput');
const guessSubmit = document.getElementById('guessEnter');
const console3Exit = document.getElementById('console3Exit');
const kilomdatabox = document.getElementById('kilomdatabox');
const moneydatabox = document.getElementById('moneydatabox');
const locationdatabox = document.getElementById('locationdatabox');
const visitedCountris = document.getElementById('countries');

// Tapahtumakäsittelijä konsolille, joka poistaa syöttökentän pelaajan syötettyä nimen,
// ja luo tilalle pelaajavalinnat

startnappula.addEventListener("click", () => {
    event.preventDefault();
    // syötetään "virhekoodi", jos pelaaja syöttää tyhjän nimen
    if (pelaajaformi.value == "") {
        emptyname.style.display = "block";
    } else {
        gameStart(pelaajaformi.value);
        emptyname.style.display = "none";
    }
})

//Tuo oikein arvattu -animaation, tällä hetkellä käyttäjän syöttäessä sijainniksi "Suomi"
function correctAnswer() {
    if (playerGuess === "Suomi") {
        document.querySelector('.goal').classList.remove('hide')
    }

}
// Tapahtumakäsittelijä oikein arvattu -animaatiolle
guessSubmit.addEventListener('click', correctAnswer)

// Tapahtumakäsittelijä, joka piilottaa animaation sitä klikatessa
document.querySelector('.goal').addEventListener('click', function (evt) {
  evt.currentTarget.classList.add('hide');
});

// pelin aloitusfunktio

async function gameStart(name) {
    document.querySelector('.konsoli1').style.display = "none";
    document.querySelector('.konsoli2').style.display = "block";
    pelaajanimi = name;
    nimiInput.innerHTML = pelaajanimi;

    const response = await fetch('http://127.0.0.1:5000/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'text':pelaajanimi})
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.nimi)
            console.log(data.rahat)
            document.getElementById("moneydatabox").innerHTML = data.rahat;
            document.getElementById("locationdatabox").innerHTML = data.sijaintimaa;
            targetCountry = data.tavoitemaa;
    })
    .catch(error => {
        console.error('Error', error);
    });
}

// exit-nappulan funktiot

const exitnappi = document.getElementById('exitButton');

exitnappi.addEventListener('click', () => {
    event.preventDefault();
    resetGame();
})

async function resetGame() {
    document.querySelector('.konsoli1').style.display = "block";
    document.querySelector('.konsoli2').style.display = "none";
    pelaajanimi = "";
    nimiInput.innerHTML = "";
    pelaajaformi.value = "";
}

// Tapahtumankäsittelijä Guess-nappulalle

async function guessCountry(guess) {
    guessForm.style.display = "block";
    playerGuess = guess;

    fetch('http://127.0.0.1:5000/veikkaa/' + playerGuess, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (playerGuess === targetCountry) {
                // tämä tuo esiin well done -animaation, toistaisesi rikki
                // document.querySelector('.goal').classList.remove('hide')

                distanceTraveled += data.lentokilometrit;
                kilomdatabox.innerHTML = parseInt(distanceTraveled);
                moneydatabox.innerHTML = data.Rahat;
                locationdatabox.innerHTML = capitalizeFirstLetter(data.sijainti)
                clearTips();
                targetCountry = data.tavoitemaa;
                GuessedRight = true;

            } else if (playerGuess !== targetCountry && data.Vihjeitä === "Jäljellä") {
                console.log("väärä veikkaus");
                // tähän väärä vastaus -animaatio
            } else if (data.Vihjeitä === "ei jäljellä") {
                document.getElementById('noTipMessage').style.display = "block";
            } else {
                // tähän väärä vastaus - animaatio ja siirtyminen seuraavaan maahan
                targetCountry = data.tavoitemaa;
                locationdatabox.innerHTML = capitalizeFirstLetter(data.sijainti);
                moneydatabox.innerHTML = data.Rahat;
                distanceTraveled += data.lentokilometrit;
                kilomdatabox.innerHTML = parseInt(distanceTraveled);
                clearTips();
                GuessedRight = false;
            }
            targetCountry = data.tavoitemaa;
        })
    console.log(playerGuess);
    guessForm.style.display = "none";
}

guessButton.addEventListener('click', () => {
    event.preventDefault();
    guessForm.style.display = "block";
})

guessSubmit.addEventListener('click', () => {
    event.preventDefault();
    guessCountry(guessInput.value);
    correctAnswer();
})

// Tapahtumankäsittelijä Tip-nappulalle
let tipindex = 1;
const tipButton = document.getElementById('tipbutton');

async function fetchTip() {
    const response = await fetch('http://127.0.0.1:5000/vihje', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            let tipID = 'tip' + tipindex;
            tipindex += 1;
            console.log(tipindex);
            console.log(tipID);
            console.log(data.vihje);
            console.log(data.rahat);
            document.querySelector('.tipbox').style.display = "block";
            document.getElementById(tipID).style.display = "block";
            document.getElementById(tipID).innerHTML = data.vihje;
            document.getElementById('moneydatabox').innerHTML = data.rahat;
        })
}

tipButton.addEventListener('click', () => {
    fetchTip()
})

// funktio vhijeiden pyyhkimiselle sivulta 
async function clearTips() {
    document.querySelector('.tipbox').style.display = "none";
    document.getElementById('tip1').style.display = "none";
    document.getElementById('tip2').style.display = "none";
    document.getElementById('tip3').style.display = "none";
    document.getElementById('tip1').innerHTML = "";
    document.getElementById('tip2').innerHTML = "";
    document.getElementById('tip3').innerHTML = "";
    tipindex = 1;
}

// maalistan funktio
async function showCountryList() {
    document.querySelector('.konsoli1').style.display = "none";
    document.querySelector('.konsoli2').style.display = "none";
    document.querySelector('.konsoli3').style.display = "block";
}

countriesButton.addEventListener('click', () => {
    event.preventDefault();
    showCountryList();
})

// maalistan exit-nappi
async function exitCountryList() {
    document.querySelector('.konsoli1').style.display = "none";
    document.querySelector('.konsoli2').style.display = "block";
    document.querySelector('.konsoli3').style.display = "none";
}

console3Exit.addEventListener('click', () => {
    event.preventDefault();
    exitCountryList();
})

// icons

// form for player name

// function to fetch data from API

// function to update game status

// function to show weather at selected airport

// function to check if any goals have been reached

// function to update goal data and goal table in UI

// function to check if game is over

// function to set up game
// this is the main function that creates the game and calls the other functions

// event listener to hide goal splash
