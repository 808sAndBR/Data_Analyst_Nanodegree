#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

# How many people
len(enron_data)

# How many features 
set([len(enron_data[x].keys()) for x in enron_data])
    
# How many person of interest
len([x for x in enron_data if enron_data[x]['poi'] ==1])

# Total stock value James Prentice owns
enron_data['PRENTICE JAMES']['total_stock_value']

# Messages from Wesley Colwell
enron_data['COLWELL WESLEY']['from_this_person_to_poi']

# Value of stock options exercised by Jeffrey K Skilling
enron_data['SKILLING JEFFREY K']['exercised_stock_options']

#Of these three individuals (Lay, Skilling and Fastow), who took home the most 
# money (largest value of “total_payments” feature)?
# How much money did that person get?

top_brass = ['Lay', 'Skilling', 'Fastow']

for person in enron_data:
    for top in top_brass:
        if top.upper() in person:
            print "%s: %s" % (person, enron_data[person]['total_payments'])


# How many folks in this dataset have a quantified salary? 
# What about a known email address?

len([x for x in enron_data if enron_data[x]['salary'] != 'NaN'])
len([x for x in enron_data if enron_data[x]['email_address'] != 'NaN'])

# How many people in the E+F dataset (as it currently exists) have “NaN” for 
# their total payments? What percentage of people in the dataset as a whole is this?

no_tot_pay = len([x for x in enron_data if enron_data[x]['total_payments'] == 'NaN'])

float(no_tot_pay)/len(enron_data)

#How many POIs in the E+F dataset have “NaN” for their total payments? 
#What percentage of POI’s as a whole is this?

pois = {x:enron_data[x] for x in enron_data if enron_data[x]['poi']}
len([x for x in pois if pois[x]['total_payments'] == 'NaN'])

# If you added in, say, 10 more data points which were all POI’s, 
# and put “NaN” for the total payments for those folks, the numbers you just 
# calculated would change. What is the new number of people of the dataset? What
# is the new number of folks with “NaN” for total payments?

10.0+len(enron_data)
no_tot_pay + 10