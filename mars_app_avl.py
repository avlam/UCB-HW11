
# coding: utf-8

# # Climate App
# UCBE HW #9
# written by: A. Lam

# Dependencies
from flask import Flask, jsonify
from scrape_mars_avl import scrape

# create Flask service
app = Flask(__name__)

# setup endpoints
base = '/api/v1.0/'

@app.route(f'{base}scrape')
def retrieve_data():
    return jsonify(scrape())

if __name__ == '__main__':
    app.run()

