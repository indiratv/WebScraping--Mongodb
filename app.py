from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)

# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# db = client.marsdatadb
# collection = db.marsdatac

@app.route("/")
def index():
    mars = mongo.db.marsdatac.find_one()
    print(mars)
    print("In the Index");
    return render_template("index.html", marsdata=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.marsdatac
    marsdata_dict_scraped = scrape_mars.scrape()
    mars.update(
        {},
        marsdata_dict_scraped,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)