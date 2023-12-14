import mysql.connector

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='projekti2',
    user='user1',
    password='password1',
    autocommit=True
    )

"""Huom. Vaihtakkee omat kirjautumistunnukset, muistakaa laittaa myös oikea projekti databaseksi"""