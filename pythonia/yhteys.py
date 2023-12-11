import mysql.connector

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='projekti2',
    user='root',
    password='veetik',
    autocommit=True
    )

"""Huom. Vaihtakkee omat kirjautumistunnukset"""