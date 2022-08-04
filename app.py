import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify

import datetime
from datetime import datetime, date


# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///horoscope.db")


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/birthday", methods=["GET", "POST"])
def birthday():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        #Приймаємо вхідні дані
        year_choose = request.form.get("year")
        month_choose = request.form.get("month")
        day_choose = request.form.get("day")
        #return jsonify(birth)

        if year_choose.isdigit() and month_choose.isdigit() and day_choose.isdigit():
            #Визначаємо хто за китайським гороскопом (за роком народження)
            year = int(year_choose) % 12
            animal_db = db.execute("SELECT animal FROM year WHERE year = ?", year)
            animal = animal_db[0]["animal"]
            link_db = db.execute("SELECT link FROM year WHERE year = ?", year)
            link_animal = link_db[0]["link"]

            #Перетворюємо місяць/день/рік народження у формат дати для подальшого використання
            dateString = day_choose+"-"+month_choose
            dateFormatter = "%d-%m"
            births = datetime.strptime(dateString, dateFormatter)
            birth = datetime.date(births)
            full_dateString = day_choose+"/"+month_choose+"/"+year_choose
            full_dateFormatter = "%d/%m/%Y"
            full_births = datetime.strptime(full_dateString, full_dateFormatter)
            full_birth = datetime.date(full_births)

            #Визначаємо хто за зодіакальним гороскопом
            zodiak_db = db.execute("SELECT symbol FROM zodiaks WHERE start <= ? AND ? <= end", birth, birth)
            zodiak = zodiak_db[0]["symbol"]
            link_zodiak = zodiak.lower()

            #Визначаємо хто за гороскопом друїдів
            druid_db = db.execute("SELECT symbol FROM druid WHERE start <= ? AND ? <= end", birth, birth)
            druid = druid_db[0]["symbol"]
            link_druid = druid.lower()

            #Визначаємо хто за Традиційним єгипетським гороскопом
            egypt_db = db.execute("SELECT symbol FROM egypt WHERE start <= ? AND ? <= end", birth, birth)
            egypt = egypt_db[0]["symbol"]
            return render_template("birthday.html", animal=animal, zodiak=zodiak, druid=druid, egypt=egypt, birth=full_birth, link_animal=link_animal, link_zodiak=link_zodiak, link_druid=link_druid)

        else:
            message = "Enter day/month/year of your birth"
            return render_template("index.html", message=message)





