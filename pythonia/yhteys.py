import mysql.connector

yhteys = mysql.connector.connect(
    host='localhost',
    port= 3306,
    database='projekti2',
    user='root',
    password='veetik',
    autocommit=True
    )

"""Huom. Vaihtakkee omat kirjautumistunnukset"""