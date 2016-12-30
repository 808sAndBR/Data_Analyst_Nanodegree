#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    import numpy as np

    cleaned_data = []

    ninety_perc = int(len(predictions) * .9)
    errors = abs(net_worths - predictions)
    keepers = sorted(errors)
    keepers = keepers[0:ninety_perc]
    cleaned_data = [(age, net_worth, error) for (age, net_worth, error)
                        in  zip(ages, net_worths, errors)
                        if error in keepers]
    
    return cleaned_data


