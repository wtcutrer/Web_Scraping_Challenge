import os
from flask import Flask, render_template
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_python

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars_data = scrape_mars_python.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/mars_data")


if __name__ == "__main__":
    app.run(debug=True)