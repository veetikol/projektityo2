from flask import Flask, request
import Vihjeet

app = Flask(__name__)
@app.route('/pelaajanimi')
def pelaajanimi():


@app.route('/ostavihje/<pelaajaolio>')
def ostaVihje():
    global vihjeindeksi
    for a in Vihjeet.countries:
        if a == päämäärä:
            print(Vihjeet.countries[päämäärä][vihjeindeksi])
            vihjeindeksi += 1
    return