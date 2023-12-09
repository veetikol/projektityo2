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

// Tapahtumakäsittelijä konsolille, joka poistaa syöttökentän pelaajan syötettyä nimen,
// ja luo tilalle pelaajavalinnat
let pelaajanimi = "";
let playerGuess = "";
let startURL = window.location.href;
let URL_with_command = "";
const pelaajaformi = document.getElementById('pelaajainput');
const startnappula = document.querySelector('#startnappula');
const nimilaatikko = document.getElementById('nimi');
const nimiInput = nimilaatikko.querySelector('p');
const emptyname = document.getElementById('emptyname');
const guessButton = document.getElementById('guessButton');
const guessForm = document.getElementById('guessForm');
const guessInput = document.getElementById('guessInput');
const guessSubmit = document.getElementById('guessEnter');

startnappula.addEventListener("click", () => {
    event.preventDefault();
    // syötetään "virhekoodi", jos pelaaja syöttää tyhjän nimen
    if (pelaajaformi.value == "") {
        emptyname.style.display = "block";
    } else {
        playerName(pelaajaformi.value);
        emptyname.style.display = "none";
    }
})

async function playerName(name) {
    document.querySelector('.konsoli1').style.display = "none";
    document.querySelector('.konsoli2').style.display = "block";
    pelaajanimi = name;
    nimiInput.innerHTML = pelaajanimi;

    fetch('htpp://127.0.0.1:3000/start', {
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
    console.log(playerGuess);
}

guessButton.addEventListener('click', () => {
    event.preventDefault();
    guessForm.style.display = "block";
})

guessSubmit.addEventListener('click', () => {
    event.preventDefault();
    guessCountry(guessInput.value);
})


// icons

// form for player name

// function to fetch data from API
async function fetchData() {
}

// function to update game status

// function to show weather at selected airport

// function to check if any goals have been reached

// function to update goal data and goal table in UI

// function to check if game is over

// function to set up game
// this is the main function that creates the game and calls the other functions

// event listener to hide goal splash
