'''
Created on 27.02.2017

@author: Gregor Hendel

run script to test different SCIPSVMSolution models on the breast cancer data set
'''

import SCIPSVMExercise as SCIPSVM
from SCIPSVMExercise import SCIPSVMLinear, SCIPSVMSparseLinear
from data.load_cancer import load_cancer
from sklearn.model_selection import train_test_split, ShuffleSplit 
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt

setup = "crossvalidation"
setup = "accuracy" # accuracy or crossvalidation

# regularization parameter for all SVM's 
C = 1.0

#
# constructor arguments for SCIP SVMs
#
# see SCIPSVMBase constructor for more information
#
constructorArguments=dict(C=C, 
                          verbosity=0, 
                          tLim=10.0, 
                          weightBound=10,
                          classWeights=[1.0,1.0])

#
# constructor for the linear Support Vector Classifier
#
linearSVCArguments=dict(dual=False, 
                        tol=1e-6,
                        penalty='l1', 
                        C=1.0)

# initialize different Support Vector Machines as triples
# (name, class, constructor arguments)
#
# for comparing the models to a standard SVM, a LinearSVC from scikitlearn is also present
# 
# more information on these classes and what they represent can be found in SCIPSVMSolution.py
svms = [\
        ("linear", SCIPSVMLinear, constructorArguments, "b"), 
         ("sparselinear", SCIPSVMSparseLinear, constructorArguments, "g"),
        ("sklearn", LinearSVC, linearSVCArguments, "k"),
        ]

dataset = load_cancer()


#
# special cross validation setup
#
C_s = np.logspace(-3, 3, 10)
ShuffleSplitArguments=dict(n_splits=10,
                           test_size=0.5,
                           random_state=42)


def computeAccuracy(svm, X, y):
    """
    Compute the accuracy of the trained SVM on a test set X,y
    
    Returns
    -------
    
    accuracy : float
        the fraction of correctly classified samples 
    """
    
    predicted = svm.predict(X)
    
    # compute the number of true positives and false negatives
    tp = sum((1 for f in range(len(y)) if y[f] > 0 and predicted[f] > 0))
    tn = sum((1 for f in range(len(y)) if y[f] < 0 and predicted[f] < 0))
    
    accuracy = (tp + tn) / (float(len(y)) + 0.0001)
    
    return accuracy

def getClassifierScores(classifier, X, y):
    """
    Return mean accuracy and standard deviation performing cross validation.
    
    Multiple values for the C penalty parameter are tested. 
    
    Parameters
    ----------
    
    classifier : classifier
        trained classifier for the current data
        
    X, y : data set
        features and labels of the training data
        
    Returns
    -------
    
    scores : list
        list of the obtained mean accuracy during cross validation 
        
    scores_std : list
        list of standard deviations around accuracy during cross validation  
        
    
    """

    scores = list()
    scores_std = list()
    shuffle_split = ShuffleSplit(**ShuffleSplitArguments)
    for C in C_s:
        classifier.C = C
        this_scores = [computeAccuracy(classifier.fit(X[train], y[train]), X[test], y[test])
             for train, test in shuffle_split.split(X)]
        
        scores.append(np.mean(this_scores))
        scores_std.append(np.std(this_scores))
        
    return scores, scores_std

def getScaledData(dataset):
    """
    Return numpy arrays of the features X and labels y
    """
    X = np.array(dataset.data)
    y = np.array(dataset.targets)
        
    # we scale the data by the mean and variance
    X = StandardScaler().fit_transform(X)
    
    return X, y
        
def evaluateAccuracy(svms):
    """
    Evaluate the given list of SVM'S on the datasets fast
    """
    X,y = getScaledData(dataset)
    
    X_train,  X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
    for name, Svmclass, args, _ in svms:
        svm = Svmclass(**args).fit(X_train, y_train)
        print "%-15s : Accuracy %.3f" % (name, computeAccuracy(svm, X_test, y_test))
            

def plotCrossValidation(svms):
    """
    cross-validate SVM's on the data set and plot the result.
    """
    pass

    fig, ax = plt.subplots(1, 1, figsize=(10,8))
    
    # loop over the two data sets, cancer, and asl
    #
    # more information about these data sets can be found in the data-subdirectory
    X, y = getScaledData(dataset)
    
    # 2. fit the different SVMs to shuffled splits and evaluate the average performance
    for name, SVMClass, args, color in svms:
        
        print name
        # 3a. Construct the classifier and fit the training data 
        svm = SVMClass(**args)            
            
        # 3b. Evaluate the classifier performance on the data using cross validation
        #
        scores, scores_std = getClassifierScores(svm, X, y) 
        ax.semilogx(C_s, scores, color, label=name)
        ax.semilogx(C_s, np.array(scores) + np.array(scores_std), '%s--'%color)
        ax.semilogx(C_s, np.array(scores) - np.array(scores_std), '%s--'%color)
        
            
    locs, labels = plt.yticks()
    plt.yticks(locs, list(map(lambda x: "%g" % x, locs)))
    plt.ylabel('CV score')
    plt.xlabel('Parameter C')
    plt.legend()
    # plt.ylim(0, 1.1)
    plt.show()
    

if __name__ == '__main__':
    # evaluate the accuracy quick or perform crossvalidation of the specified models.    
    if setup == "accuracy":
        evaluateAccuracy(svms)
    elif setup == 'crossvalidation':
        plotCrossValidation(svms)
    
