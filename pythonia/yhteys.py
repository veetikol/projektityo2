import mysql.connector

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='prokkis2',
    user='root',
    password='veetikol',
    autocommit=True
    )

"""Huom. Vaihtakkee omat kirjautumistunnukset, muistakaa laittaa myös oikea projekti databaseksi"""