#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 08:10:22 2021

@author: shauangel
"""
#flask
from flask import jsonify, Flask, request, render_template

#modules
from FASTA import FASTA
from systemParse import ABCpred, BcePred, BCPREDS, Bepipred2, LBtope, LEPS
import votefunc

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('main.html')


@app.route('/prediction', methods=['POST'])
def prediction():
    if request.method == 'POST':
        
        #get data from website
        data = request.get_json()
        print(data)
        
        #create FASTA class obj & analyze seq
        fasta = FASTA(data['data'])
        
        fasta.get_organism_name()
        
        #start prediction system
        result = {}
        
        for sys, f in data['range'].items():
            single_sys = {}
            single_result = {}
            
            #choose system
            if sys == 'LEPS':
                system = LEPS()
            elif sys == 'ABCPred':
                system = ABCpred()
            elif sys == 'Bcepred':
                system = BcePred()
            elif sys == 'BCpreds':
                system = BCPREDS()
            elif sys == 'BepiPred-2':
                system = Bepipred2()     
            elif sys == 'LBtope':
                system = LBtope()
            else:
                continue
            
            for name, seq in fasta.result.items():
                protein = {'PREDS' : "", 't-coffee' : ""}
                protein['PREDS'] = system.parse_web(seq)
                protein['t-coffee'] = fasta.tcoffee_seq[name]
                single_result[name] = protein
                
            if sys == 'LBtope':
                temp = system.get_result(single_result)
                single_result = temp
                
                
            single_sys['data'] = single_result
            single_sys['f'] = f
            result[sys] = single_sys
        
        test = votefunc.vote_func({'sys' : result, 
                                   'min_length' : data['shortest'],
                                   'range' : 0.5})
        return jsonify(test)
    
    return 'err'

if __name__ == "__main__":
    app.run()
















