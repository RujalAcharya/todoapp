from flask_pymongo import PyMongo
from flask import Flask, flash, render_template,redirect,url_for
from form import InsertForm
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase2"
app.config["SECRET_KEY"] = "r83648732647832684fsd"

mongo = PyMongo(app)
collectio = mongo.db.collection

@app.route('/', methods = ['GET','POST'])
def insert():
    form = InsertForm()
    if form.validate_on_submit():
        flash(f'New Data inserted', 'sucess')
        newDict = {}
        newDict['title'] = form.title.data
        newDict ['Description'] = form.description.data
        if form.done.data == True:
            newDict['Status'] = 'Done'
        else:
            newDict['Status'] = 'Not Done'
        collectio.insert(newDict)
    return render_template('index.html', incomplete_collec=collectio.find({'Status': 'Not Done'}),  complete_collec=collectio.find({'Status': 'Done'}),title='Insert',form=form)

@app.route('/update/<el>', methods = ['GET', 'POST'])
def update(el):
    el = ObjectId(el)
    collec = mongo.db.collection
    form = InsertForm()
    itemToUpdate = collec.find_one({"_id":el})
    if form.validate_on_submit():
        newDict = {}
        if form.done.data == True:
            newDict['Status'] = 'Done'
        else:
            newDict['Status'] = 'Not Done'
        print(newDict)
        collec.update_one(itemToUpdate, {"$set": newDict})
        return redirect('/')
    form.title.data = itemToUpdate['title']
    form.description.data = itemToUpdate['Description']
    return render_template('index.html', form= form)



@app.route ('/complete/<el>', methods = ['GET','POST'])
def complete(el):
    el = ObjectId(el)
    itemToUpdate = collectio.find_one ({"_id":el})
    collectio.delete_one(itemToUpdate)
    itemToUpdate['Status'] = 'Done'
    collectio.insert_one(itemToUpdate)
    return redirect('/')

@app.route ('/delete/<el>', methods=['GET','POST'])
def delete(el):
    el = ObjectId(el)
    collectio.delete_one({"_id": el})
    return redirect('/')

if __name__=='__main__':
    print("todolist")
    app.run(debug=True)
