   
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_python

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    mars = mongo.db.mars.find_one()
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars = scrape_mars_python.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)