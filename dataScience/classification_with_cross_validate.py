#from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import make_moons
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from datetime import datetime
from inspect import stack
from matplotlib import pyplot as plt

import pandas as pd
import numpy as np
import sklearn
import re
import sys
import warnings
warnings.filterwarnings('ignore')

class CwCV:
    """
    Abstract class for classification_with_cross_validate
    Holds mostly the properties (attributes) and does the initial 
    parsing of input parameters
    """
    def __init__(self, *args, **kwargs):
        # SETS ALL THE DEFAULTS HERE!
        self.df          = kwargs.get("df", None) # MUST COME FIRST!
        self.activation  = kwargs.get("activation", "logistic")
        self.target      = kwargs.get("target", "target")
        self.features    = kwargs.get("features", None) # Must come after self.target
        self.k           = kwargs.get("k", 5)
        self.folds       = kwargs.get("folds", 5)
        self.read_csv_delimiter = kwargs.get("delimiter", None)
        self.hidden_layer_sizes = kwargs.get("hidden_layer_sizes", tuple())
        self.overfit            = kwargs.get("overfit", 0.99)
        self.underfit           = kwargs.get("underfit", 0.05)
        self.classifier         = kwargs.get("classifier", "knn") # Always comes last!!!!!

    def _is_list_of_strings(self, value):
        if not isinstance(value, (list, tuple)): 
            return False
        for s in value:
            if not isinstance(s, str): 
                return False
        return True
            
    def _is_list_of_ints(self, value):
        if not isinstance(value, (list, tuple)): 
            return False
        for s in value:
            if not isinstance(s, int): 
                return False
        return True

    @property 
    def classifier(self):
        try: return self.CLASSIFIER
        except (AttributeError, ValueError):
            err = "Attribute {} is not set. ".format(str(stack()[0][3]))
            raise ValueError(err)
        
    @classifier.setter
    def classifier(self, value):        
        # k-nearest-neighbors
        if isinstance(value, sklearn.neighbors.classification.KNeighborsClassifier):
            self.CLASSIFIER = value
            self.CLASSIFIER_TYPE = "knn"
        elif re.match("^kn.*$", str(value).lower()):
            self.CLASSIFIER = KNeighborsClassifier(n_neighbors=self.k)
            self.CLASSIFIER_TYPE = "knn"
        
        # Neural net
        elif isinstance(value, sklearn.neural_network.multilayer_perceptron.MLPClassifier):
            self.CLASSIFIER = value
            self.CLASSIFIER_TYPE = "mlp"
        elif re.match("^mlp.*$", str(value).lower()):
            self.CLASSIFIER = MLPClassifier(hidden_layer_sizes=self.hidden_layer_sizes, activation=self.activation)
            self.CLASSIFIER_TYPE = "mlp"

        else:
            err = "Classifier of type '{}' for attribute {} is not yet available. ".format(type(value), str(stack()[0][3]))
            raise NotImplementedError(err)
    
    @property
    def df(self):
        try: return self.DF
        except (AttributeError, ValueError):
            err = "Attribute {} is not set. ".format(str(stack()[0][3]))
            raise ValueError(err)        

    @df.setter
    def df(self, value):
        if isinstance(value, pd.core.frame.DataFrame):
            self.DF = value
        
        elif isinstance(value, sklearn.utils.Bunch):
            # Convert a built in sklearn bunch to a pandas df
            try: self.DF = pd.DataFrame(np.c_[value["data"]])
            except Exception as e:
                err = "Attribute {} was unable to convert 'value' of type '{}' to a pandas DataFrame. (value = {}) [{}]".format(
                    str(stack()[0][3]),
                    type(value),
                    str(value), 
                    str(e)
                    )
                raise ValueError(err)

        elif isinstance(value, str):
            try:
                if self.read_csv_delimiter is None:
                    self.DF = pd.read_csv(value)
                else:
                    self.DF = pd.read_csv(value, delimiter = read_csv_delimiter)
            except Exception as e:
                err = "Attribute {} was unable to 'read_csv({}) to a pandas DataFrame. [{}]".format(
                    str(stack()[0][3]),
                    str(e)
                    )
                raise ValueError(err)

    @property
    def features(self):
        try: return self.FEATURES
        except (AttributeError, ValueError):
            err = "Attribute {} is not set. ".format(str(stack()[0][3]))
            raise ValueError(err)
    
    @features.setter
    def features(self, value):
        err = "Attribute {} must be a list of strings, with each string holding the name of a target column. (value = {})".format(str(stack()[0][3]), str(value) )
        # Must be a list of string column names
        if value is None:
            # Accepts all columns as features except for whats in the target list
            self.FEATURES = [c for c in self.df.columns if c not in self.target]
        
        elif isinstance(value, str):
            self.FEATURES = [value]

        elif isinstance(value, (list, tuple)):
            if not self._is_list_of_strings(value):
                raise ValueError(err)
            self.FEATURES = value
        
        else:
            raise ValueError(err)
            
    @property 
    def folds(self):
        try: return self.FOLDS
        except (AttributeError, ValueError):
            err = "Attribute {} is not set. ".format(str(stack()[0][3]))
            raise ValueError(err)
    
    @folds.setter 
    def folds(self, value):
        if isinstance(value, int): 
            self.FOLDS = value
        else:
            err = "Attribute {} must be an integer. (value = {})".format(str(stack()[0][3]), str(value))
            raise ValueError(err)

    @property
    def hidden_layer_sizes(self):
        try: return self.HLF
        except (AttributeError, ValueError):
            err = "Attribute {} is not set. ".format(str(stack()[0][3]))
            raise ValueError(err)

    @hidden_layer_sizes.setter
    def hidden_layer_sizes(self, value):
        if self._is_list_of_ints: 
            self.HLF = value
        else:
            err = "Attribute {} must be a list or tuple of integers. (value = {})".format(str(stack()[0][3]), str(value))
            raise ValueError(err)            

    @property 
    def k(self):
        try: return self.K
        except (AttributeError, ValueError):
            err = "Attribute {} is not set. ".format(str(stack()[0][3]))
            raise ValueError(err)
    
    @k.setter 
    def k(self, value):
        if isinstance(value, int): 
            self.K = value
        else:
            err = "Attribute {} must be an integer. (value = {})".format(str(stack()[0][3]), str(value))
            raise ValueError(err)

    @property 
    def overfit(self):
        try: return self.OVERFIT
        except (AttributeError, ValueError):
            err = "Attribute {} is not set. ".format(str(stack()[0][3]))
            raise ValueError(err)
    
    @overfit.setter 
    def overfit(self, value):
        err = "Attribute {} must be an int between 0 and 100, or a float between 0 and 1 (value = {})".format(str(stack()[0][3]), str(value))
        
        if not isinstance(value, (int, float)):
            raise ValueError(err) 

        elif value < 0:
            raise ValueError(err) 
        
        elif value > 1: 
            self.OVERFIT = (value/100)

        else:
            self.OVERFIT = value
    
    @property 
    def underfit(self):
        try: return self.UNDERFIT
        except (AttributeError, ValueError):
            err = "Attribute {} is not set. ".format(str(stack()[0][3]))
            raise ValueError(err)
    
    @underfit.setter 
    def underfit(self, value):
        err = "Attribute {} must be an int between 0 and 100, or a float between 0 and 1 (value = {})".format(str(stack()[0][3]), str(value))
        
        if not isinstance(value, (int, float)):
            raise ValueError(err) 

        elif value < 0:
            raise ValueError(err) 
        
        elif value > 1: 
            self.UNDERFIT = (value/100)

        else:
            self.UNDERFIT = value

    @property
    def target(self):
        try: return self.TARGET
        except (AttributeError, ValueError):
            err = "Attribute {} is not set. ".format(str(stack()[0][3]))
            raise ValueError(err)
    
    @target.setter
    def target(self, value):
        err = "Attribute {} must be a list of strings, with each string holding the name of a target column. (value = {})".format(str(stack()[0][3]), str(value) )
        # Must be a list of string column names
        if isinstance(value, str):
            self.TARGET = [value]
        
        elif isinstance(value, (list, tuple)):
            if not self._is_list_of_strings(value):
                raise ValueError(err)
            self.TARGET = value
        
        else:
            raise ValueError(err)
            
        
class classification_with_cross_validate(CwCV):
    """
    :NAME:
        classification_with_cross_validate()
        
    :DESCRIPTION:
        classification_with_cross_validate() is a quick and dirty way to run a classification
        via cross validation and get some mildly useful output. 
    
    :PARAMETERS:
        
        classifier: Sets the type of classifier.  
                    DEFAULT: k-nearest-neighbor
        
        df:         All work is done based on a Pandas DataFrame. df accepts an existing
                    DataFrame, a path to load a CSV as a DataFrame, or an sklearn test 
                    Bunch (sklearn.utils.Bunch, I.e. df = sklearn.datasets.load_digits() )
             
        features:   A list or tuple containing string names of columns to be used as features.
                    DEFAULT: All columns except the 'target' column(s).
        
        target:     A list or tuple containing string names of columns to be used as target(s).
                    DEFAULT: A columns named 'target'.
            

        folds:      An integer to determine how many folds to be used with 
                    sklearn.model_selection.cross_validate.
                    DEFAULT: 5
                    

        hidden_layer_sizes: Valid for MLPClassifier only. A list or tuple containing the hidden layer 
                            sizes. I.e. (8,8,10,)
                            If passed in for other than a MLPClassifier classifier, the attribute is ignored.  
                            DEFAULT: None
        
        k:          Valid for k-nearest-neighbor. The 'k' value as an integer.  
                    If passed in for other than a k-nearest-neighbor classifier, the attribute is ignored.  
                    DEFAULT: 5
        
        overfit:    Is based on the ACTUAL AVERAGE VALUE returned for the 'training set' from within 
                    sklearn.model_selection.cross_validate. I.e. 0.99 will consider an average value 
                    of 0.99 OR GREATER from the AVERAGE cross_validate_scores['train_score']
                    as an overfit condition. 
                    
                    NOTE: This is informational only, and no impact on the running of the tests. 

        underfit:   Is based on the DIFFERENCE between the average values returned for the 'test set' 
                    and 'train set' from within sklearn.model_selection.cross_validate. I.e. 0.05 will 
                    consider a difference of 0.05 OR GREATER between the average values for the 
                    test and training results as an underfit condition. 
                    
                    NOTE: This is informational only, and no impact on the running of the tests. 

    :METHODS:
        run:      After parameters are set, this runs the actual fit, predictions, validations - and
                  returns the results. 
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run(self):        
        cv_scores = cross_validate(self.classifier, self.df[self.features], self.df[self.target], cv=self.folds, return_train_score = True)
        avgtest  = np.mean(cv_scores['test_score'])
        avgtrain = np.mean(cv_scores['train_score'])
        diff = abs(avgtest - avgtrain)
        fit = "probably OK"
        
        if diff > self.underfit: 
            fit = "maybe underfit?"
        
        if np.mean(cv_scores['train_score']) > self.overfit: 
            fit = "overfit" 
        
        # Build message
        message = "\nClassifier: {} [{}] "
        msg_activation = self.activation
        
        if self.CLASSIFIER_TYPE == "mlp":
            message += "hidden Layers:{}\n"
            msg_hidden_Layers = self.hidden_layer_sizes
        else:
            message += "{}\n"
            msg_hidden_Layers = ""

        
        message += " cv_test_scores: {}(avg={})\n cv_train_scores:{}(avg={}) \n diff = {} [{}]"
        
        print(message.format(
                            self.CLASSIFIER_TYPE,
                            msg_activation,
                            msg_hidden_Layers,
                            cv_scores['test_score'],
                            avgtest,
                            cv_scores['train_score'], 
                            avgtrain,
                            diff,
                            fit
                            )
        )
                
                
            
if __name__ == '__main__':
    from sklearn.datasets import load_digits
    c = load_digits()
    o = classification_with_cross_validate(df = c)
    o.df["target"] = c["target"]
    o.k = 5
    o.folds = 4
    o.overfit = 1
    o.underfit = .07
    o.classifier = "MLP"
#    o.classifier = "knn"
    
    for activation in ["logistic", "relu"]:
        o.activation = activation 
        for neuron in [8, 32, 128]:
            o.hidden_layer_sizes = (neuron,neuron,neuron,)  
            o.run()
    
    
    
    
    