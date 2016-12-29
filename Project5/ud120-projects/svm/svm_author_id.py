#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

#clf = SVC(kernel = 'linear')
clf = SVC()

# sample the data
features_train = features_train[:len(features_train)/100] 
labels_train = labels_train[:len(labels_train)/100] 

t0 = time()
clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"

t1 = time()
pred = clf.predict(features_test)
print "prediction time:", round(time()-t1, 3), "s"

accuracy_score(pred, labels_test)

for c_value in [10.0, 100.0, 1000.0, 10000.0]:
    clf = SVC(C = c_value)
    clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)
    accuracy = accuracy_score(pred, labels_test)    
    print "%s accuracy: %s" % (c_value, accuracy)
    
features_train, features_test, labels_train, labels_test = preprocess()  

clf = SVC(C = 10000)
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
accuracy = accuracy_score(pred, labels_test)    
print "accuracy: %s" % accuracy

pred[10]
pred[26]
pred[50]

sum(pred == 0)
sum(pred == 1)


#########################################################


