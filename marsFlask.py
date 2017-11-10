from flask import Flask, jsonify, render_template, redirect
import scrape_mars
import pymongo
import subprocess
import os

# Flask setup
app = Flask(__name__)

@app.route("/")
def welcome():
    # """List all available api routes."""
    print("Retrieving homepage")

    mongod = subprocess.Popen(
        "mongod --dbpath {0}".format("c:\data\db"),
        shell=False
    )
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.webscrape
    collection = db.mars

    mars = collection.find_one()
    print(mars)
    mongod.terminate()

    # return render_template("test2.html", dict=mars)

    return render_template("index.html", dict=mars)
    

@app.route("/scrape")
def scrape():
    print('Scraping Mars data...')

    # if we don't do this, we need to manually kick off mongod in cmd line
    mongod = subprocess.Popen(
        "mongod --dbpath {0}".format("c:\data\db"),
        shell=False
    )
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.webscrape
    collection = db.mars

    # db.collection.insert_one(scrape_mars.scrape())
    
    data = scrape_mars.scrape()

    collection.update(
        {},
        data,
        upsert=True
    )

    mongod.terminate()

    return redirect("http://localhost:5000/", code=302)

if __name__ == '__main__':
    app.run(debug=True)