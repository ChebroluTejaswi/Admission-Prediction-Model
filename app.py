# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import math
import pickle
app = Flask(__name__) # initializing a flask app

# --------------------------------------------------------------------------------------------------------------------------
@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")
# --------------------------------------------------------------------------------------------------------------------------

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            # reading the inputs given by the user
            gre_score=float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            is_research = request.form['research']
            if(is_research=='yes'):
                research=1
            else:
                research=0
            X=[]
            X.append(gre_score)
            X.append(toefl_score)
            X.append(university_rating)
            X.append(sop)
            X.append(lor)
            X.append(cgpa)
            X.append(research)
            Y=[]
            Y.append(X)

            filename = 'finalized_model.pickle'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            loaded_standaradization = pickle.load(open("standardization.pickle",'rb'))
            # predictions using the loaded model file
            prediction=loaded_model.predict(loaded_standaradization.transform(Y)) # not correct
            
            print('prediction is', prediction)
            
            # showing the prediction results in a UI
            return render_template('results.html',prediction=round(100* prediction[0]))

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    else:
        return render_template('index.html')
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	app.run(debug=True) # running the app