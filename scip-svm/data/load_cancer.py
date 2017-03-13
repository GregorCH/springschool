'''
Created on 27.02.2017

@author: Gregor Hendel
'''
import csv
import os

class DataSet:
    '''
    dummy class to assign data and targets to
    '''
    pass

def load_cancer():
    '''
    returns an object with two properties - 'data' for the features and 'targets' as labels
    '''
    with open(os.path.join(os.path.dirname(__file__), "wdbc.data"), "r") as currfile:
        reader = csv.reader(currfile)
        rawdata = [row for row in reader]

        data = []
        targets = []
        labelmap = {'M':1, "B":-1}
        for d in rawdata:
            data.append(map(float, d[2:]))
            targets.append(labelmap[d[1]])
        ds = DataSet()
        ds.data = data
        ds.targets = targets
    return ds

if __name__ == "__main__":
    ds = load_cancer()
    for d in ds.data:
        print d
    print ds.targets
    