#!/usr/bin/python3

from api_calls import all_calls
from flask import Flask, render_template, flash, url_for, request
import asyncio



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def homepage():
    'calls the api necessary for homepage'
    result = asyncio.run(all_calls())
    return render_template('home.html', result=result)



if __name__ == '__main__':
    app.run(debug=True)
