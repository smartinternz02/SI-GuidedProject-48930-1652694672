from flask import Flask, render_template, request
import numpy as np
import pickle


app = Flask(__name__,template_folder='templates')
model = pickle.load(open('regression.pkl', 'rb'))


@app.route('/')
def intro():
    return render_template('index.html')


@app.route('/y_predict',methods=["POST", "GET"])
def prediction():
    cylinders= request.form["cylinders"]
    displacement = request.form["displacement"]
    horsepower = request.form["horsepower"]
    weight = request.form["weight"]
    acceleration = request.form["acceleration"]
    modelyear = request.form["modelyear"]
    origin= request.form["origin"]
    total=[[int(cylinders),int(displacement),int(horsepower),int(weight),int(acceleration),int(modelyear),int(origin)]]
    prediction = model.predict(total)
    output=prediction[0]
    if(output<=10):
        pred="Based on mileage it delivers worst performance  " + str(prediction[0]) +" would require extra fuel to be carried at all times"
    if(output>10 and output<=18):
        pred="Based on mileage it delivers low performance " +str(prediction[0]) +" not advisable to travel long distances"
    if(output>18 and output<=30):
        pred="Based on mileage it delivers medium performance" +str(prediction[0]) +" can go to nearby places"
    if(output>30 and output<=47):
        pred="Based on mileage it delivers high performance " +str(prediction[0]) +" can go to distant places"
    if(output>47):
        pred="Based on mileage it delivers best performance " +str(prediction[0])+" suitable for very long travel as well"

    return render_template("index.html",predicted_output='{}'.format(pred))


if __name__ == '__main__':
    app.run(debug=True, port=900)
