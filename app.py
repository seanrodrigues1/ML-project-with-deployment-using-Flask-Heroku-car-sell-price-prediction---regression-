# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 00:09:55 2023

@author: seanr
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__,template_folder='template_files')
model = pickle.load(open('rf_regressor_model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index_1.html')


#standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        no_of_years=2020-Year
        
        Present_Price=float(request.form['Present_Price'])
        
        Kms_Driven=int(request.form['Kms_Driven'])
        
        Owner=int(request.form['Owner'])
        
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesal'): 
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            
       
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
            
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
            
        prediction=model.predict([[Present_Price,Kms_Driven,Owner,no_of_years,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index_1.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index_1.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index_1.html')

if __name__=="__main__":
    app.run(debug=True)