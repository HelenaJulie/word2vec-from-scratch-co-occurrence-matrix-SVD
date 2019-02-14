# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 06:53:28 2019

@author: helen
"""

# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import re
import sys
#--- CONSTANTS ----------------------------------------------------------------+
class word2vec():
    def __init__ (self):
         self.script = sys.argv[0]
         self.filename= sys.argv[1]
         self.window= int(sys.argv[2])
         #reading file and convertinf to lower case and removing special characters
         s = open(self.filename, "r").read().lower()
         st=re.sub('[^a-zA-Z0-9 \n]', '', s)
         self.corpus=st.split() 
         for i in range(0,self.window):
             self.corpus=["#"]+self.corpus
             self.corpus.append("#")
         self.U=[]
         pass
    
    def data_preparation(self):

        self.no_of_total_words = len(self.corpus) 
        
        self.unique_words_list = []

          # generate unique words    
        for word in self.corpus:     
            if word not in self.unique_words_list:
                if word!="#":
                    self.unique_words_list.append(word)
        
        self.no_of_unique_words = len(self.unique_words_list)

        self.cooccurrence_matrix=np.zeros((self.no_of_unique_words,self.no_of_unique_words+1))
        pass
    
    def generate_cooccurrence_matrix(self):
        for i, word in enumerate(self.unique_words_list):
            for pos, w in enumerate(self.corpus):
                if (w==word):
                    for j in range(pos-self.window, pos+self.window+1):
                        if j!=pos and j<=self.no_of_total_words-1 and j>=0:
                            w1=self.corpus[j]
                            if w1=="#":
                                k=0
                            else:
                                k=self.unique_words_list.index(w1)+1
                            self.cooccurrence_matrix[i][k]=self.cooccurrence_matrix[i][k]+1
        #normalize
        for i in range(0,len(self.cooccurrence_matrix)):
            count=0
            for j in range(0,len(self.cooccurrence_matrix[i])):
                count=count + self.cooccurrence_matrix[i][j]
            for j in range(0,len(self.cooccurrence_matrix[i])):
                self.cooccurrence_matrix[i][j]=self.cooccurrence_matrix[i][j]/count
        pass
    
    def reduce_dimensionality(self):
        la=np.linalg
        self.U,S,Vh=la.svd(self.cooccurrence_matrix,full_matrices=False)
        for i in range(0,len(self.U)):
            for j in range(0,len(self.U[0])):
                self.U[i][j]=round(self.U[i][j],5)
        pass
    def print_output(self):
        output_matrix=np.zeros((len(self.U),self.window*2))
        for i in range(0,len(self.U)):
            for j in range(0,self.window*2):
                output_matrix[i][j]=self.U[i][j]
        f= open("out.txt","w+")
        for i in range(0,len(output_matrix)):
            for j in range(0,len(output_matrix[0])):
                f.write("{0:.5f} \t".format(round(output_matrix[i][j],5)))
            f.write("\n")
        f.close()
        pass

w2v = word2vec()

data = w2v.data_preparation()
w2v.generate_cooccurrence_matrix()
w2v.reduce_dimensionality()
w2v.print_output()
print("Execution completed... Check out.txt file")