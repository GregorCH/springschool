'''
Created on 27.02.2017

@author: Gregor Hendel

Module that contains several discrete models for training Support Vector Machines with SCIP

The class SCIPSVMBase represents the logic for all the models and implements the 
interface functions fit() and predict()

All derived subclasses represent a specialization that implement their own side constraints
to train, e.g., a sparse SVM (such that only few of the features are selected) or to model
a discrete ramp loss function using binary variables as indicator variables.
'''

from pyscipopt import Model, quicksum
import numpy

class SCIPSVMBase:
    '''
    base class for all derived SCIP based Support Vector Machines
    
    SCIPSVMBase is the base class of all different SCIPSVM... classes
    It provides the interface methods fit() and predict()
    
    Subclasses must override the method addModelFormulation()
    '''
         
    def __init__(self, C=.125, tLim=5.0, verbosity=0, sparsity = .2, weightBound=10.0, classWeights=[1.0, 1.0]):
        """
        Construct a SCIP SVM object.
        
        Parameters
        ----------        
        C : float >= 0
            objective weight for misclassification of examples
            
        tLim : float >= 0
            time limit in seconds for the optimization (default: 5.0 seconds)
            
        verbosity : int
            integer between 0 and 5 to control the verbosity of SCIP output (default: 0)
            
        sparsity : float
            fraction between 0 and 1 of feature dimensions that can be nonzero. This is optional
            and does not have to be respected by all derived sub classes
            
        weightBound : float > 0
            bound on the absolute of the omega variables (feature weights) 
            
        classWeights : list of length 2
            penalty objective weights for classes -1 and 1 
        """
        
        if type(classWeights) is not list or len(classWeights) != 2:
            return ValueError("'classWeights' argument must be a list of length 2")
        
        if weightBound <= 0 or tLim <= 0 or C <= 0:
            return ValueError("'C', 'tLim' and 'weightBound' arguments must be positive floats")
        
        if not 0.0 <= sparsity <= 1.0:
            return ValueError("'sparsity' argument must be between 0.0 and 1.0")
         
        self.C = C
        self.tLim = tLim
        self.verbosity = verbosity
        self.sparsity = sparsity
        self.weightBound = weightBound
        self.classWeights= classWeights
        
    def predict_single(self, X):
        """
        Classify a single example based on its features
        
        Parameters
        ----------
        
        X : list or iterable 
           feature vector to classify
           
        Returns
        -------
        
        y : float
           class prediction for X. Negative means class -1, Positive means class 1
        """
        
        return self.offset + sum((self.weights[f] * X[f] for f in xrange(len(X)))) 
    
    def predict(self, X):
        """
        Classify multiple examples.
        
        Parameters
        ----------
        
        X : list or iterable 
           feature vector to classify
           
        Returns
        -------
        
        y : list
           list of length len(X) with a float that represents the classification of this example
        """
        result = map(self.predict_single, X)
        return result
    
    def initializeWeights(self, nfeatures):
        """
        Initialize trivial weights that always predict class 1.
        
        Parameters
        ----------
        
        nfeatures : int
            positive integer that describes the dimension of the feature space
        """
        
        self.nfeatures = nfeatures
        self.weights = [0.0] * self.nfeatures 
        self.offset = 1.0

    def fit(self, X, Y):
        '''
        Fit SVM model to data given as features of shape (nexamples, nfeatures) and labels Y.
        
        Parameters
        ----------
        
        X : list
            training example features of shape (nexamples, nfeatures)
            
        Y : list
            class label, either -1 or 1, for every training example
            
        Returns
        -------
        
        self : SCIPSVMBase subclass
            the calling object itself for efficient pipelines
        '''
        
        
        self.model = Model("SCIP-SVM")
        self.model.setRealParam("limits/time", self.tLim)
        self.model.setIntParam("display/verblevel", self.verbosity)
        self.initializeWeights(len(X[0]))
        self.nexamples = len(Y)
                
        try:
            
            self.addProblemVariables()
            self.addObjectiveFunction(X, Y)
            self.addModelFormulation(X, Y)
            
                
            self.model.optimize()
            
            sols = self.model.getSols()
            
                        
            if sols:
                self.weights = [self.model.getSolVal(sols[0], self.omegas[f]) for f in xrange(self.nfeatures)]
                self.offset = self.model.getSolVal(sols[0], self.omegas[self.nfeatures])
            
        except NotImplementedError:
            pass
            
        return self
    
    def addProblemVariables(self):
        """
        Add problem variables respecting the chosen attribute "rampLoss"
        
        Add all problem variables required for the feature weights and the (discrete) ramp loss
        depending on the chosen "rampLoss"
        """
        
        raise NotImplementedError("This function should be implemented as an exercise")
        
        # add feature weight variables. add an additional offset
        self.omegas = []
        
        
        # add variables xi to penalize misclassification
        self.xis = []
        
    
    def addObjectiveFunction(self, X, y):
        """
        Add the objective function as a quadratic constraint that bounds an artificial objective variable.
        
        Parameters
        ----------
        
        X : list
            list of training examples, each example a feature vector list of the same dimension
             
        y : list
            labels, either -1 or 1 for each training example
        """
        
        raise NotImplementedError("Implement this function as an exercise")
        
        # add artifical objective function variable
        self.artobjvar = None
        
        # apply correction to account for unequal proportions of positive and negative example
        objCoeffs = [1.0 for yi in y]
        
        name="objective_function"
    
    def addModelFormulation(self, X, y):
        """
        Enrich the model by variables and the necessary constraints
        
        Parameters
        ----------
        
        X : list
            training samples with shape (nexamples, nfeatures)
        y : list 
            labels {-1, 1} for every example 
        """
        raise NotImplementedError("This method must be provided by derived subclasses")
    
class SCIPSVMLinear(SCIPSVMBase):
    """
    simple linear SVM without discrete decisions
    """
    def addModelFormulation(self, X, y):
        SCIPSVMBase.addModelFormulation(self, X, y)
        
class SCIPSVMSparseLinear(SCIPSVMBase):
    """
    linear SVM that uses additional, binary variables to enforce sparsity
    """
    
    rampLoss = False
    
    
    def addModelFormulation(self, X, y):
        SCIPSVMBase.addModelFormulation(self, X, y)
        
        # add linear misclassification constraints
            
        # use binary variables to enforce sparsity, and restrict the number of v variables that can be one
        vs = []