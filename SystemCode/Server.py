from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import sys
import os
import json
import Trainer as trainer
import Classifier as classifier
import pandas as pd


app = Flask(__name__, static_url_path='/static')

# app = Flask(__name__, static_folder='build', static_url_path='/build')
app = Flask(__name__, template_folder="build", static_folder="build/static")


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
uploadDir= 'uploads'

# @app.route("/")
# def index():
 
    #return "Welcome to Traige Artificial Intelligence Module"
    #return app.send_static_file('index.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """ This is a catch all that is required for react-router """
    return render_template('index.html')


@app.route('/upload', methods = ['POST'])  
def upload_success():  

    data = {}

    if request.method == 'POST': 
      
        try:
            f = request.files['file']  
            id = request.form['id']  
            file = os.path.splitext(f.filename)

            print("i am upload"+str(id))
            print("i am file"+str(id))
            try:
                f.save(uploadDir+'//'+id+'//'+id+file[1])  
            except FileNotFoundError as fnfe:
                os.mkdir(uploadDir+'//'+id)
                f.save(uploadDir+'//'+id+'//'+f.filename)  
            data['message'] = "File uploaded successfully"
        except Exception as ex:
            print(ex)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            data['error'] = "Exception occured"
            #print(message) 
            # return "Indexsss!@ss!!"

    #return render_template("success.html", name = "123") 
    return jsonify(data)

@app.route('/train/<int:id>', methods = ['POST'])  

def train(id):  
    data = {}
    try:
        print("training"+str(id))
        inputFilePath = uploadDir+'//'+str(id)+'//'+str(id)+".csv"
        outputClassifierFilePath = uploadDir+'//'+str(id)+'//'+str(id)+".joblib"
        outputVectorFilePath = uploadDir+'//'+str(id)+'/features.pkl'
        
        print(inputFilePath)
        print(outputClassifierFilePath)
        result = trainer.train(inputFilePath,outputClassifierFilePath,outputVectorFilePath)

        subdata = {}
        subdata['msg'] = "Training completed successfully"
        subdata['result'] =result
        data['message'] = subdata


    # to update status to jtraige
    except Exception as ex:
            print(ex)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            data['error'] = "Exception occured"
    print(data)
    #return render_template("success.html", name = "123") 
    return jsonify(data)

@app.route('/<int:userid>/check', methods = ['POST'])  
def check_success(userid):  
    data = {}
    try:
        print("check"+str(userid))
        ticketId = request.form['id']  
        details = request.form['details']
        timestamp = request.form['timestamp'] 
        print(id)
        print(details)
        print(timestamp)
        # initialize list of lists 
        newdata = [[details]] 
      
        # Create the pandas DataFrame 
        df = pd.DataFrame(newdata, columns = ['sentence']) 

        modelFilePath = uploadDir+'//'+str(userid)+'//'+str(userid)+".joblib"
        featuresFilePath = uploadDir+'//'+str(userid)+'/features.pkl'
        dataFilePath= uploadDir+'//'+str(userid)+'//'+str(userid)+".data"
        df.to_csv(dataFilePath, index = False)
        predictedPriority = classifier.check(featuresFilePath,modelFilePath,dataFilePath)
        print(predictedPriority)
        data['message']={}
        data['message']['id']=ticketId
        data['message']['priority']=int(predictedPriority)
    except Exception as ex:
            print(ex)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            data['error'] = "Exception occured"
    #return render_template("success.html", name = "123") 
    return jsonify(data)

if __name__ == "__main__":
	app.run(debug=True, host='127.0.0.1', port=9001)


