from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars 
import os

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb+srv://mongo_user:8Z20sQQ31JANA1FW@cluster0.p3kvz.mongodb.net/mars?retryWrites=true&w=majority")

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()    
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)