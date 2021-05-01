# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Internal file imports
from scrape_mars import scrape


# create instance of Flask app
app = Flask(__name__)


# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/visit_mars_app")



# create route that renders index.html template
@app.route("/")
def index():

    mars_data = mongo.db.mars_data_collection.find()
    for data in mars_data:
        data_res = data

    #team_list = ["Jumpers", "Dunkers", "Dribblers", "Passers"]
    return render_template("index.html", my_dict_data=data_res)




@app.route("/scrape")
def scraper():
    mars_data_collection = mongo.db.mars_data_collection
    mars_data_dict = scrape()
    mars_data_collection.update({}, mars_data_dict, upsert=True)
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)
