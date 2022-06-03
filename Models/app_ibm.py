from flask import Flask, render_template, request
import numpy as np
# import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "lzvVjuXgmUKxoSIR5xkFsvexxqCGxXOZd4EkR2a2iHPj"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)
# model = pickle.load(open('regression.pkl', 'rb'))


@app.route('/')
def intro():
    return render_template('index.html')


@app.route('/y_predict',methods=["POST"])
def prediction():
    cylinders= request.form["cylinders"]
    displacement = request.form["displacement"]
    horsepower = request.form["horsepower"]
    weight = request.form["weight"]
    acceleration = request.form["acceleration"]
    modelyear = request.form["modelyear"]
    origin= request.form["origin"]
    total=[[int(cylinders),int(displacement),int(horsepower),int(weight),int(acceleration),int(modelyear),int(origin)]]
    # prediction = model.predict(total)
    # output=prediction[0]
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [
        {"fields": [["f0", "f1", "f2", "f3", "f4", "f5", "f6"]], "values": total}]}
    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/309ed04f-6b22-434b-ae54-b5a3804c0d9f/predictions?version=2022-06-02',
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    # print(response_scoring.json())
    pred = response_scoring.json()
    output = pred['predictions'][0]['values'][0][0]
    print(output)
    pred1 = str(output)
    # if(output<=10):
    #     pred1="Based on mileage it delivers worst performance  " + str(output[0][0]) +" would require extra fuel to be carried at all times"
    # if(output>10 and output<=18):
    #     pred1="Based on mileage it delivers low performance " +str(output[0][0]) +" not advisable to travel long distances"
    # if(output>18 and output<=30):
    #     pred1="Based on mileage it delivers medium performance" +str(output[0][0]) +" can go to nearby places"
    # if(output>30 and output<=47):
    #     pred1="Based on mileage it delivers high performance " +str(output[0][0]) +" can go to distant places"
    # if(output>47):
    #     pred1="Based on mileage it delivers best performance " +str(output[0][0])+" suitable for very long travel as well"

    return render_template("index.html",predicted_output='{}'.format(pred1))


if __name__ == '__main__':
    app.run(debug=False)
