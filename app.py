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
    
@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))
    
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id" : ObjectId(task_id)})
    all_catagories = mongo.db.catagories.find()
    return render_template("edit_task.html", task=the_task, categories=all_catagories)
    
@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))
    
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({"_id" : ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

@app.route('/categories')
def get_categories():
    all_catagories = mongo.db.catagories.find()
    return render_template("categories.html", categories=all_catagories)

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    the_category = mongo.db.catagories.find_one({"_id" : ObjectId(category_id)})
    return render_template("edit_category.html", category=the_category)
    
@app.route('/update_category/<category_id>', methods=["POST"])
def update_category(category_id):
    categories = mongo.db.catagories
    categories.update( {'_id': ObjectId(category_id)},
    {
        'category_name':request.form.get('category_name')
    })
    return redirect(url_for('get_categories'))
    
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.catagories.remove({"_id" : ObjectId(category_id)})
    return redirect(url_for('get_categories'))
    
@app.route('/add_category')
def add_category():
    return render_template("add_category.html")

@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.catagories
    categories.insert_one(request.form.to_dict())
    return redirect(url_for('get_categories'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)