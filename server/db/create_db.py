# -*- coding: utf-8 -*-
"""
@author Bruno Dias

"""

import sqlite3

conn = sqlite3.connect('Issues.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys")

cursor.execute("""
CREATE TABLE Zona_de_Conforto_Lab(
        zona_conforto_id INT NOT NULL PRIMARY KEY,
        temp_min FLOAT NOT NULL,
        temp_max FLOAT NOT NULL,
        umid_min FLOAT NOT NULL,
        umid_max FLOAT NOT NULL,
        lum_min FLOAT NOT NULL,
        lum_max FLOAT NOT NULL);
""")

cursor.execute("""
CREATE TABLE Lab(
        lab_id INT NOT NULL PRIMARY KEY,
        zona_conforto_id INT NOT NULL REFERENCES Zona_de_Conforto_Lab(zona_conforto_id),
        nome CHAR(20) NOT NULL,
        endereco CHAR(30) NOT NULL,
        intervalo_parser INT NOT NULL,
        intervalo_arduino INT NOT NULL);
""")

cursor.execute("""
CREATE TABLE Log_Lab(
        data INT NOT NULL PRIMARY KEY,
        lab_id INT NOT NULL REFERENCES Lab(lab_id),
        temp FLOAT NOT NULL,
        umid FLOAT NOT NULL,
        lum FLOAT NOT NULL);
""")

cursor.execute("""
CREATE TABLE Equip(
        equip_id INT NOT NULL PRIMARY KEY,
        lab_id INT NOT NULL REFERENCES Lab(lab_id),
        temp_min FLOAT NOT NULL,
        temp_max FLOAT NOT NULL,
        end_mac CHAR(29) NOT NULL);
""")

cursor.execute("""
CREATE TABLE Log_Equip(
        data INT NOT NULL PRIMARY KEY,
        equip_id INT NOT NULL REFERENCES Equip(equip_id),
        temp FLOAT NOT NULL);
""")

cursor.execute("""
CREATE TABLE User_Lab(
        user_id CHAR(4) NOT NULL PRIMARY KEY,
        nome CHAR(30) NOT NULL,
        email CHAR(30) NOT NULL,
        data_aprov TIMESTAMP);
""")

cursor.execute("""
CREATE TABLE Presenca(
        presenca_id INT PRIMARY KEY,
        user_id CHAR(4) NOT NULL REFERENCES User_Labs(user_id),
        lab_id INT NOT NULL REFERENCES Lab(lab_id),
        presente BOOLEAN NOT NULL);
""")

cursor.execute("""
CREATE TABLE Log_Presenca(
        data INT NOT NULL PRIMARY KEY,
        user_id CHAR(4) NOT NULL REFERENCES User_Labs(user_id),
        lab_id INT NOT NULL REFERENCES Lab(lab_id),
        evento CHAR(3) NOT NULL);
""")

cursor.execute("""
CREATE TABLE User_Sys(
        user_id INT NOT NULL PRIMARY KEY,
        login CHAR(10) NOT NULL,
        senha CHAR(16) NOT NULL,
        email CHAR(30) NOT NULL,
        nome CHAR(30) NOT NULL,
        admin BOOLEAN NOT NULL);
""")

conn.close()