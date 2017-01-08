#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from sklearn.tree import DecisionTreeClassifier

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'other', 'bonus', 'expenses', 'total_payments',
                    'total_stock_value', 'to_messages']
                    
### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
# please see POI_writeup.ipynb

### Task 3: Create new feature(s)
# created in POI_writeup.ipynb but not used in final model

### Store to my_dataset for easy export below.
from collections import defaultdict
my_dataset = defaultdict(dict)

for person in data_dict:
    for field in data_dict[person]:
        if field in features_list:
            my_dataset[person][field] = data_dict[person][field]

for person in my_dataset:
    for field in my_dataset[person]:
        if my_dataset[person][field] == 'NaN':
            my_dataset[person][field] = 0

# outliers = ['LAY KENNETH L']

# my_dataset = {person:my_dataset[person] for person in my_dataset if person not in outliers}
### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
# My exploration is in POI_writeup.ipynb using final model below

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=None,
            max_features='auto', max_leaf_nodes=None, min_samples_leaf=1,
            min_samples_split=1, min_weight_fraction_leaf=0.0,
            presort=False, random_state=1809, splitter='best')

# from sklearn.ensemble import AdaBoostClassifier
# clf = AdaBoostClassifier(algorithm='SAMME.R', base_estimator=None,
#           learning_rate=1.5, n_estimators=20, random_state=1809)
            
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(
    features, labels, test_size=0.3, random_state=1809)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)