from geopy.distance import geodesic
from yhteys import yhteys
from flask import Flask, request, Response
import json
import random


class Player:
    def __init__(self):
        self.nimi = ""
        self.rahat = 1000
        self.sijaintimaa = "Finland"
        self.sijaintiairport = "Helsinki Vantaa Airport"
        self.lentokm = 0
        self.tavoitemaa = ""
        self.vihjeindeksi = 0


class Game:
    def __init__(self, listasanakirja):
        self.maat = []
        self.lentokentat = []
        self.listaindeksi = 0
        self.vihjeet = listasanakirja


"""Yllä olevat oliot ovat datan ylläpitämistä varten. Käytönnössä kaikki pelissä esiintyvät
muuttujat ovat osa olioita.
Tämä sen takia, että pelin voisi tallentaa jossain vaiheessa, ja funktioiden parametrit ovat olioita.
"""

# ALla kaikki sanakirjarakenteet, eli vihjeet, maat ja lentokentät


luxembourghints = ["1. The Second richest country in the world",
                   "2. The name of this country starts with a word from latin, which means “light”",
                   "3. The Smallest country in Benelux"]
norwayhints = ["1. The most successful country in Winter Olympics",
               "2. This country has the highest standard of living in the world",
               "3. This country shares border with 3 other countries but it has more coastline than land border."]
polandhints = ["1. The biggest country in eastern middle-europe", "2. The flag of this country is like Pokemon ball",
               "3. During WWII. Germany built concentration camps in this country"]
swedenhints = ["1. Dancing queen", "2. The world leading furniture company was founded in this country",
               "3. This country is always one step ahead of Finland"]
latviahints = ["1. The jeans were invented in this country", "2. This country is sandwiched by other baltic countries",
               "3. The capital of this country is Riga"]
lithuaniahints = ["1. This country is known from its amber jewellery", "2. The biggest baltic country",
                  "3. The capital of this country is Vilnius"]
spainhints = ["1. One of the biggest symbol of this country is a bull",
              "2. You can go to Africa with a ferry from this country in 1 hour",
              "3. The Finnish tourists have invaded this country"]
albaniahints = ["1. The flag of this country has 2 headed eagle on it",
                "2. This European country is one of the last ones that doesn’t have McDonalds",
                "3. 70% of this country is mountain area and its located opposite side of the “high heel”"]
bulgariahints = ["1. The Europes poorest country", "2. This country uses cyrillic alphabet",
                 "3. The capital of this country is Sofia"]
icelandhints = ["1. This country is the westernmost nordic country", "2. This country is home to the artist Björk",
                "3. This country has hot springs"]
belgiumhints = ["1. This country's flag has the same colors as the flag of Germany",
                "2. This country, instead of France, invented french fries",
                "3. This country is often associated and mixed with France"]
germanyhints = ["1. This country's history in the World War II is very controversial",
                "2. This country is a major hub of the automotive industry",
                "3. This country is right in the middle of Europe"]
estoniahints = ["1. This country was last one to become independent from Soviet Union",
                "2. This country is a neighbour country of Finland", "3. This country's capital is Tallinn"]
finlandhints = ["1. This country is known for one of the most successful mobile phone businesses in the world",
                "2. This country is constantly ranked as one of the world's happiest countries",
                "3. This country has a very strong sauna culture"]
ukhints = ["1. This country is known for bands like Blur", "2. This country is not a part of the EU",
           "3. This country is home to fish and chips"]
irelandhints = ["1. This country is known for it’s pub culture", "2. This country is home to leprechauns",
                "3. This country’s capital is Dublin"]
croatiahints = ["1. Best football player of the year 2018 chosen by FIFA born here",
                "2. The famous dessert with bananas references to one of the biggest cities in this country",
                "3. One of the filming places for Game Of Thrones"]
francehints = ["1. A significant country in the world of fashion art",
               "2. The Disney animation about a cooking mouse is based on this country",
               "3. Known for its over 300 meters long tower"]
greecehints = ["1. This country has the third oldest language in the world",
               "2. A country known for the development of philosophy",
               "3. This country is the birthplace of the modern Olympics"]
italyhints = ["1. Leads UNESCO's statistics on world heritage sites",
              "2. Milla Magia lives on the slopes of a famous volcano in this country",
              "3. This country is known worldwide for its delicious pizza and pasta"]
sloveniahints = ["1. World famous 'Postojna' cave system is located in this country",
                 "2. This country is mainly mountainous, and more than 90 percent of the country is more than 200 meters above sea level",
                 "3. The capital of this country is a charming city named Ljubljana"]
czechrepublichints = ["1. World known ice-hockey player with a iconic mullet haircut was born here",
                      "2. Federation which splitted into two separated countries in 1993",
                      "3. Pilsner beer originates from this country"]
maltahints = ["1. Is known by taxfree casino licenses", "2. This country consista by many islands",
              "3. World's tenth-smallest country. With a total area of 316 squeare kilometers"]
hungaryhints = ["1. This country is known by its traditional spicy meat soup", "2. Local currency is known as HUF",
                "3. Tonava river splits this country at the middle"]
austriahints = ["1. Samuli Edelmann has drunk wine in this country",
                "2. Most of the landscape of this country consists of the Alps",
                "3. In which country was Mozart born in?"]
portugalhints = ["1. This country is known for its portwines", "2. This country is the 2016 football European champion",
                 "3. This country is located at the tip of the Iberian peninsula"]
romaniahints = ["1. The Carpathian mountain range runs through the middle of this country.",
                "2. The currency used in this country is leu",
                "3. The famous region of Transylvania is located in this country"]
netherlandshints = ["1. This country is known for its EDM culture", "2. This country is known for its coffee shops",
                    "3. This countrys capital is Amsterdam"]
switzerlandhints = ["1. This country is well known for their policy of neutrality",
                    "2. This country is well known for its culture of watch-making",
                    "3. The Red Cross was founded in this country"]
belarushints = ["1. This country's official dish is called draniki",
                "2. This country's president is the longest serving president in Europe",
                "3. This country's capital is Minsk"]
northmacedoniahints = ["1. This country changed its name as recently as 2019", "2. This country’s flag depicts a sun.",
                       "3. This country’s capital city is Skopje"]
ukrainehints = ["1. This country is the second biggest country in Europe",
                "2. This country's currency is called hryvnia", "3. This country is on an ongoing war with russia"]
serbiahints = ["1. This country has the worlds oldest Orthodox church, the Sopočan monastery",
               "2. This country is a landlocked country, located east of Bosnia & Herzegovina",
               "3. This country’s capital is Belgrade"]
montenegrohints = ["1. This country’s name means The black mountain in English",
                   "2. This country uses the euro as its currency, even thought it is not part of the Eurozone",
                   "3. This country is located next north of Albania"]
russiahints = ["1. This country sold the region of Alaska to USA in 1867",
               "2. This country has the largest population in Europe", "3. This is the largest country in the world"]
slovakiahints = ["1. This country used to be a joint state with the Czech Republic.",
                 "2. This country’s flag has a double cross ", "3. This country’s capital city is Bratislava"]
denmarkhints = ["1. This country is known for a very popular toy manufacturer", "2. This country is a nordic country",
                "3. This countrys capital is Copenhagen"]

hints = (luxembourghints, norwayhints, polandhints, swedenhints, latviahints, lithuaniahints,
         spainhints, albaniahints, bulgariahints, icelandhints, belgiumhints, germanyhints,
         estoniahints, finlandhints, ukhints, irelandhints, croatiahints, francehints,
         greecehints, italyhints, sloveniahints, czechrepublichints, maltahints, hungaryhints,
         austriahints, portugalhints, romaniahints, switzerlandhints, northmacedoniahints, serbiahints,
         montenegrohints, ukrainehints, belarushints, russiahints, slovakiahints, denmarkhints, netherlandshints)

countries = {"luxembourg": luxembourghints, "norway": norwayhints, "poland": polandhints, "sweden": swedenhints,
             "latvia": latviahints,
             "lithuania": lithuaniahints, "spain": spainhints, "albania": albaniahints, "bulgaria": bulgariahints,
             "iceland": icelandhints,
             "belgium": belgiumhints, "germany": germanyhints, "estonia": estoniahints, "finland": finlandhints,
             "united kingdom": ukhints,
             "ireland": irelandhints, "croatia": croatiahints, "france": francehints, "greece": greecehints,
             "italy": italyhints,
             "slovenia": sloveniahints, "czech republic": czechrepublichints, "malta": maltahints,
             "hungary": hungaryhints, "austria": austriahints, "portugal": portugalhints,
             "romania": romaniahints, "switzerland": switzerlandhints, "belarus": belarushints,
             "north macedonia": northmacedoniahints, "serbia": serbiahints, "ukraine": ukrainehints,
             "montenegro": montenegrohints, "russia": russiahints, "slovakia": slovakiahints, "denmark": denmarkhints,
             "netherlands": netherlandshints}

country_names = ["luxembourg", "norway", "poland", "sweden", "latvia", "lithuania", "spain",
                 "albania", "bulgaria", "iceland", "belgium", "germany", "estonia", "finland", "united kingdom", "uk"
                                                                                                                 "ireland",
                 "croatia", "france", "greece", "italy", "slovenia", "czech republic", "malta", "hungary", "austria",
                 "portugal", "romania"
                             "switzerland", "belarus", "serbia", "ukraine", "montenegro", "russia", "slovakia",
                 "denmark", "north macedonia"]


# Yllä kaikki tietorakenteet. Muutetaan pääohjelmassa järkevämpään muotoon olioiden ominaisuuksiksi
# ALla olevaa funktiota muutettu hieman alkuperäisestä. Jättää Suomen pois


def maat():
    sql = "SELECT LOWER(country.name), airport.name FROM country, airport"
    sql += " WHERE airport.iso_country = country.iso_country AND country.iso_country != 'FI' AND country.continent = 'EU' AND airport.type = 'large_airport' GROUP BY country.name"
    kursori = yhteys.cursor(buffered=True)
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos


# ALla hieman muutettu versio haevihje-funktiosta. Palauttaa vihjeen stringinä, koska pitää siirtää sivulle json.

def haevihje(pelaaja, peli):
    tuloste = ""  # Tyhjä tuloste
    for a in peli.maat:  # Käydään lista maista läpi. TÄhän on varmaan parempi tapa olemassa.
        if a == pelaaja.tavoitemaa:  # Jos maa on tavoitemaa, siirrytään suoritukseen
            # tuloste = (countries[päämäärä][vihjeindeksi])
            tuloste = peli.vihjeet[pelaaja.tavoitemaa][pelaaja.vihjeindeksi]  # Tallettaa vihjeen tuloste-muuttujaan
            pelaaja.vihjeindeksi += 1  # Vihjeindeksi kasvaa, kun oikea vihje tallessa
            pelaaja.rahat -= 100  # Rahaa lähtee
    return tuloste  # Palauttaa vihjeen stringinä


# TÄtä voi käyttää pohjana, kun tehdään uutta lentokilsojen laskemista.

def calculateDistance(pelaaja, peli):
    search1 = f"SELECT latitude_deg, longitude_deg FROM airport"
    search1 += f" WHERE name = '{pelaaja.sijaintiairport}' AND type = 'large_airport';"
    peli.listaindeksi += 1
    search2 = f"SELECT latitude_deg, longitude_deg FROM airport"
    search2 += f" WHERE name = '{peli.lentokentat[peli.listaindeksi]}' AND type = 'large_airport';"
    kursori = yhteys.cursor()
    kursori.execute(search1)
    tulos1 = kursori.fetchone()
    kursori.execute(search2)
    tulos2 = kursori.fetchone()
    distance = geodesic(tulos1, tulos2).km
    return distance


pelaaja = Player()
peli = Game(countries)  # Luodaan taustapalvelun käynnistyessä peli- ja pelaaja-oliot

"""sqlhaku = maat()
random.shuffle(sqlhaku)
# maalista = []
# lentokenttälista = []
for x in sqlhaku:
    peli.maat.append(x[0])

for y in sqlhaku:
    peli.lentokentat.append(y[1])"""

# Yllä olevat 6 riviä hakee ne maat ja lentokentät, ja järjestää randomisti kahteen eri listaan
# Listat ovat Game-olion sisällä, jotta ne olisi helpompi tallentaa myöhemmin

# Alla pelin aloitusfunktio. Saadaan sivulta pelaajan nimi, ja asetetaan tavoitemaa. Palautetaan tarvittava data


app = Flask(__name__)


@app.route('/start/<nimi>')
def start(nimi, pelaaja, peli):
    sqlhaku = maat()
    random.shuffle(sqlhaku)
    for x in sqlhaku:
        peli.maat.append(x[0])
    for y in sqlhaku:
        peli.lentokentat.append(y[1])
    pelaaja.nimi = nimi
    pelaaja.tavoitemaa = peli.maat[peli.listaindeksi]
    vastaus = {
        "nimi": pelaaja.nimi,
        "rahat": pelaaja.rahat,
        "sijainti": pelaaja.sijaintimaa,
        "kohdemaa": pelaaja.tavoitemaa  # Tämä saattaa olla turha
    }
    return vastaus  # Palautetaan vastaus json-muodossa.


"""
@app.route('/vihje/<location>')
def haevihje(location):
    päämäärä = location
    vihje = haevihje(päämäärä)
    vastaus = {
        "vihje": vihje
    }
    return vastaus


"""


@app.route('/vihje')
def vihjeenosto(pelaaja, peli):
    vihje = haevihje(pelaaja, peli)
    vastaus = {
        "vihje": vihje,
        "rahat": pelaaja.rahat

    }
    return vastaus


# Ylläoleva funktio hakee vihjeen, ja palauttaa sen ja päivittyneen rahatilanteen json-muodossa. Muu nettisivulla oleva
# tieto ei päivity

@app.route('/veikkaa/<veikkaus>')
def veikkaa(pelaaja, peli, veikkaus):
    if pelaaja.tavoitemaa == veikkaus:
        pelaaja.rahat += 100
        pelaaja.vihjeindeksi = 0
        kayty = pelaaja.tavoitemaa
        pelaaja.sijaintiairport = peli.lentokentat[peli.listaindeksi]
        pelaaja.sijaintimaa = pelaaja.tavoitemaa  # Pelaajan sijainti vaihtuu tavoitemaaksi
        lentomatka = calculateDistance(pelaaja,
                                       peli)  # Pelaajan lentomatka lasketaan. Vihjeindeksi kasvaa funktion sisällä
        pelaaja.lentokm += lentomatka  # pelaajan lentokilometreihin lisätään lentomatka
        pelaaja.tavoitemaa = peli.maat[peli.listaindeksi]

        vastaus = {
            "Vastaus": "Oikein",
            "Rahat": pelaaja.rahat,
            "sijainti": pelaaja.sijaintimaa,
            "lentokenttä": pelaaja.sijaintiairport,
            "tavoitemaa": pelaaja.tavoitemaa,
            "lentokilometrit": pelaaja.lentokm,
            "käyty maa": kayty

        }
        return vastaus

    else:
        if pelaaja.vihjeindeksi == 2:
            pelaaja.sijaintimaa = pelaaja.tavoitemaa
            pelaaja.sijaintiairport = peli.lentokentat[peli.listaindeksi]
            lentomatka = calculateDistance(pelaaja, peli)
            pelaaja.lentokm += lentomatka
            pelaaja.rahat -= 100
            pelaaja.vihjeindeksi = 0

            pelaaja.tavoitemaa = peli.maat[peli.listaindeksi]

            vastaus = {
                "Vastaus": "Väärin",
                "Vihjeet": "Loppu",
                "Rahat": pelaaja.rahat,
                "sijainti": pelaaja.sijaintimaa,
                "lentokenttä": pelaaja.sijaintiairport,
                "tavoitemaa": pelaaja.tavoitemaa,
                "lentokilometrit": pelaaja.lentokm

            }
            return vastaus

        else:
            vihje = haevihje(pelaaja, peli)
            vastaus = {
                "Vastaus": "Väärin",
                "Vihjeitä": "Jäljellä",
                "Rahat": pelaaja.rahat,
                "Vihje": vihje

            }

            return vastaus


""""@app.route('/save')
def tallenna(pelaaja, peli):
    # Eli tähän tulee sql-update-lause, joka tallentaa nykyisen pelitilanteen sql-tietokantaan.
"""



if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)

"""Eli peliä on muutettu niin, että pyritään pitämään olioissa (pelaaja ja peli) kaikki data. 
Tällä hetkellä valmiina on start-flask, ostavihje-flask ja veikkaa-flask. Pelin pitäisi ainakin paperilla
toimia näillä funktioilla. 

Tällä hetkellä puuttuu vielä ainakin random event peliin, ja pelin tallennus. Periaatteessa se tallennus
on suht yksinkertainen, mutta työläs. Databasea pitää muokata hieman sen toimimista varten
(Pitää siis lisätä game-taulu, johon päivitetään peli-olion tiedot.)

Lisäksi puuttuu kokonaan se lentokilometrien laskeminen. Vanhan funktion pitäisi toimia pienillä muokkauksilla.

Bugeja todennäköisesti tulee löytymään, kun kokeillaan frontin ja backendin yhdistämistä, mutta life is life.

"""











