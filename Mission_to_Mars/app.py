# Import Dependencies
from flask import Flask, render_template, redirect
import pymongo
from pymongo import MongoClient
import scrape_mars
import os

# Create MongoDB connection
# Create database and collection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client["mars_db"]
collection = db["marsdata"]

# Create an instance of Flask app
app = Flask(__name__)

# Create home route
@app.route("/")
def index():
    mars_info = db.collection.find_one()
    return render_template("index.html", mars_info=mars_info)

# Create route to scrape and import scraped data
@app.route("/scrape")
def scrape():
    
    mars_info = db.collection
    mars_data = scrape_mars.scrape()
    mars_info.update({},mars_data,upsert=True)
    return redirect("http://127.0.0.1:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)