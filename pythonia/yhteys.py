import mysql.connector

yhteys = mysql.connector.connect(
    host='localhost',
    port= 3306,
    database='prokkis2',
    user='root',
    password='veetikol',
    autocommit=True
    )

"""Huom. Vaihtakkee omat kirjautumistunnukset"""