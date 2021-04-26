#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 08:35:29 2021

@author: shauangel
"""
import re
from tcoffee import tcoffee


class FASTA:
    result = {}
    fasta = []
    tcoffee_seq = {}
    
    def __init__(self, file):
        self.input_file = file
        fasta = re.split(r'(>)', file)
        index = [d for d, s in enumerate(fasta) if s == ">" ]
        self.fasta = [ fasta[ind]+fasta[ind+1] for ind in index]
        m_aln = tcoffee()
        self.tcoffee_seq = m_aln.parse_web(file)
    
    def get_organism_name(self):
        for f in self.fasta:
            pattern = re.compile(r'[[](.*?)[]]', re.S)
            self.result[re.findall(pattern, f)[0]] = f
            
    
    
            
    

