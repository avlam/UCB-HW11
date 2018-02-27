
# coding: utf-8

# # Climate App
# UCBE HW #9
# written by: A. Lam

# Dependencies
from flask import Flask, jsonify, render_template
import pymongo
from scrape_mars_avl import mongo_mars, scrape

# Create Flask service
app = Flask(__name__)

# Create Mongo Database
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars

# Setup endpoints
base = '/api/v1.0/'

@app.route(f'{base}')
def home():
    mars = list(db.mars.find())[0]
    return render_template('index.html',mars = mars)

@app.route(f'{base}scrape')
def refresh():
    mongo_mars()
    mars = list(db.mars.find())[0]
    return render_template('index.html',mars = mars)

@app.route(f'{base}test')
def retrieve_data():
    return jsonify(scrape())

if __name__ == '__main__':
    app.run()

