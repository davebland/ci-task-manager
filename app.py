import os
import json
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Get creds from untracked file
with open('mongo_creds.txt') as creds:
    data = json.load(creds)
    app.config['MONGO_DBNAME'] = data['MONGO_DBNAME']
    app.config['MONGO_URI'] = data['MONGO_URI']

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())
    
@app.route('/add_tasks')
def add_tasks():
    return render_template("add_task.html", categories=mongo.db.catagories.find())
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)