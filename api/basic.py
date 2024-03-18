from flask import (Flask, render_template, redirect, 
                   url_for,request, session, flash, send_file, jsonify)
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'



def get_data(n):
    url = f'https://api.thingspeak.com/channels/2463512/feeds.json?api_key=YQCFGPBD34UONLYE&results={n}'
    response = requests.get(url)
    response = response.json()
    #pprint.pprint(response)

    feeds = response["feeds"]

    return feeds

def format_date(date):
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    datetime_object = datetime.strptime(date, date_format) + timedelta(hours=1)
    date = datetime_object.strftime("%Y-%m-%d %H:%m")
    return date


def update_feeds(feeds):
    for i,v in enumerate(feeds):
        n = {
            'created_at': format_date(v['created_at']),
            'field1': str(round( float(v['field1']) -0.8, 2)),
            'field2': str(round( float(v['field2']), 2)),
            'field3': v['field3'],
            'field4': v['field4'],
            'field5': v['field5']
        }
        feeds[i] = n
        

    return feeds


@app.route('/')
def index():
    return render_template('home.html', feeds=[])

@app.route('/fetch_data/<int:number>')
def fetch_data(number):
    feeds = get_data(number)
    feeds = update_feeds(feeds)
    feeds.reverse() # reverse data

    return render_template('home.html', feeds=feeds)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)