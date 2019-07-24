#%matplotlib inline
from abc import ABC
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn import linear_model # For LinearRegression

import regression_exceptions as err
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import inspect

def log(value):
    print(value)

class regression_abstract(ABC):
    @property
    def orig_df(self):
        return self.ORIGDF
    
    @orig_df.setter
    def orig_df(self, value):
        if isinstance(value, pd.core.frame.DataFrame):
            self.ORIGDF = value
            self.df     = self.ORIGDF
        else: 
            raise ValueError("'orig_df' must be a pandas dataframe [Value={}]".format(type(value)))        

    @property
    def df(self):
        return self.DF
    
    @df.setter
    def df(self, value):
        """"""
        if value is None: 
            try: 
                self.DF # see if its set
                return # do nothing
            except: 
                raise err.DFPropetyNotSetException()
        
        if isinstance(value, pd.core.frame.DataFrame):
            self.DF = value
        else: 
            raise ValueError("'df' must be a pandas dataframe [Value={}]".format(type(value)))        

    @property
    def k(self):
        try: 
            return self.K
        except (AttributeError, ValueError)as e:
            self.K = 0
            return self.K
        
    @k.setter
    def k(self, value):
        try: self.K = int(value)
        except ValueError as e: 
            raise ("Parameter  'k' must be an integer (value = {}).".format(str(value)))
             
    @property
    def train_df(self):
        return self.TRAIN
    
    @train_df.setter
    def train_df(self,value):
        self.TRAIN = value

    @property
    def test_df(self):
        return self.TEST 

    @test_df.setter
    def test_df(self,value):
        self.TEST = value

    @property
    def features(self):
        try: 
            return self.FEATURES
        except:
            try:
                self.FEATURES = self.df.columns.to_list()
                return self.FEATURES
            except Exception as e: 
                raise err.DFPropetyNotSetException() 
        
    @features.setter
    def features(self,value):
        """
        self.FEATURES should always end up as a list
        """
        if value is None: 
            try: 
                self.FEATURES
                return # self.FEATURES exists so do nothing
            except (NameError, AttributeError): 
                # Try to derive from DataFrame
                try: 
                    self.FEATURES = self.df.columns.to_list()
                    if "Saleprice" in self.FEATURES: print("Its here. ") #333
                except:
                    raise err.DFPropetyNotSetException("The parameter 'features' could not be derived from the existing default DataFrame.")
        
        elif isinstance(value, (pd.core.indexes.base.Index)):
            self.FEATURES = value.to_list()
        
        elif isinstance(value, (tuple, list)):
            self.FEATURES = list(value)

        else: 
            raise ValueError("'features' must be list, tuple, or pandas DataFrame.columns objec [Value={}]".format(type(value)))        
                    
    @property
    def mse(self):
        return self.MSE
    
    @mse.setter
    def mse(self,value):
        if isinstance(value, (list,tuple)):
            self.MSE = value
        else:
            self.MSE = [value]

    @property
    def rmse(self):
        return self.RMSE
    
    @rmse.setter
    def rmse(self,value):
        if isinstance(value, (list,tuple)):
            self.RMSE = value
        else:
            self.RMSE = [value]
    
    @property
    def predictions(self):
        return self.PREDICTIONS
    
    @predictions.setter
    def predictions(self, value):
        self.PREDICTIONS = value

    @property
    def target(self):
        return self.TARGET
    
    @target.setter
    def target(self, value):
        if not isinstance(value, (tuple,list)): value = [value]
        for col in value:
            if col not in self.df.columns:
                raise ValueError("The target column '{}' does not appear to be in the Dataframe from '{}'.".format(col, self.path))
        self.TARGET = value
#         self.all_features_except(value)

    @property
    def train_percent(self):
        return self.TRAINPER
    
    @train_percent.setter
    def train_percent(self, value):
        if value < 0: raise ValueError("train_percent must be between 0 and 1, or a real number (for number of rows to use for training.)[value = {}]".format(type(value)))
        self.TRAINPER = value

    @property
    def train_row_num(self):
        # Set the real number of rows used for train/test
        try: return self.TRAINROWNUM
        except:
            # Set to default value
            self.train_row_num = 0.5
            return self.TRAINROWNUM

    @train_row_num.setter
    def train_row_num(self, value):
        # Set the real number of rows used for train/test
        if value > 1: 
            self.TRAINROWNUM = value
        else: 
            self.TRAINROWNUM = int(self.df.shape[0]* value)
                
    @property
    def interpolate(self):
        return self.INTERPOLATE
    
    @interpolate.setter
    def interpolate(self, value):
        # Ensure boolean
        self.INTERPOLATE = True if value else False

    @property
    def carry_forward(self):
        return self.CARRYFORWARD
    
    @carry_forward.setter
    def carry_forward(self, value):
        # Ensure boolean
        self.CARRYFORWARD = True if value else False
    
    
class regression(regression_abstract):
    """
    :NAME: 
        (Class)regression
        
    :DESCRIPTION:
        A useful series of tools for managing regression tests from a pandas DataFrame
        
    :PROPERTIES:
    
    :METHODS:
        train_and_test( df = None,
                        features = None, 
                        target = "SalePrice", 
                        train_percent = .5, 
                       ):
                       
        transform_features( df = None, 
                            features = None, 
                            drop = None, 
                            percent_missing = .25
                            ):
    """
    def __init__(self, 
                 path = r"/home/rightmire/WinDocuments/tmp/AmesHousing.tsv", 
                 delim = "\t"
                ):
        self.path = path
        self.orig_df = self.df = pd.read_csv(path, delimiter="\t")
        self.lr = linear_model.LinearRegression()

    #===========================================================================
    # def all_features_except(self, target = []):
    #     if not isinstance(target, (tuple,list)): value = list(target)
    #     self.features = []
    #     for col in self.df.columns:
    #         if col in target: continue
    #         self.features.append(col)
    #     return self.features
    #===========================================================================

    def _convert_to_dummies(self, column, force = False):
        def _convert():
            codes = pd.Categorical(self.df[col]).codes
            # Create dummy values that can be correlated
            newcol = pd.get_dummies(pd.Categorical(self.df[col]))
            self.df[col] = newcol

        if (self.df[col].dtype == np.float64 or self.df[col].dtype == np.int64):
            if force == True:
                _convert()
                print("Numeric column {} forcibly converted.".format(col))
                return
            else:
                print("Column {} is numeric. Skipping dummies conversion.".format(col))
        else:
            _convert()
            print("Column {} converted.".format(col))

    def _cross_validation(self):
        """"""
        self.df = self.df[self.features] # Dump all rows but those contained in features
        self.df = self.df.dropna(axis = 1) # Drop columns with NAN values
        self.make_numerical_df(categorical = False)
        self.df = self.df.sample(frac = 1) # shuffle the df locally
        self.features = self.df.columns.to_list()
#         self.features = self.features + self.target
        self.train_row_num = self.train_percent # Get the split for training/testing
        #
        result = []
        # Split into folds
        folds = {}
        previous_fold = 0
        for fold in range(self.train_row_num, self.df.shape[0], self.train_row_num): # Theoretically every row could be a fold 
            folds[fold] = self.df[previous_fold:fold]
            previous_fold = fold

        kf = KFold(n_splits=self.k, shuffle=True)
        print("self.target = ", self.target)
        for train_index, test_index, in kf.split(self.df):
            train_df = self.df.iloc[train_index]
            test_df  = self.df.iloc[test_index]
            result.append(self._train_and_test(train_df, test_df) )
        self.rmse = result
        return result

    def _holdout(self):
        # Set local dataframe
#         df, features, target = self._roll_inplace(df, features, target)
        #=======================================================================
        # self.train_percent  = train_percent 
        # # Set the real number of rows used for train/test
        # if self.train_percent > 1: 
        #     train_row_num = train_percent
        # else: 
        #     train_row_num = int(self.df.shape[0]* train_percent)
        #=======================================================================
        # switch to local DF copy
        self.df = self.df.dropna(axis = 1) # Drop columns with NAN values
#         print("df na values=", df.isnull().sum())#333
        self.df = self.df.select_dtypes(include=['integer', 'float'])
        # Pull train and test rows
        # Use self train/self.test for global reference
        train_df = self.df[:self.train_row_num]
        self.features = train_df.columns
        test_df = self.df[self.train_row_num:]
        ## You can use `pd.DataFrame.select_dtypes()` to specify column types
        ## and return only those columns as a data frame.
        return self._train_and_test(train_df, test_df)
#===============================================================================
#         numeric_columns = self.numeric_columns(self.train_df)
#         numeric_train_df = self.train_df[numeric_columns]
#         numeric_test_df  = self.test_df[ self.numeric_columns(self.test_df) ]
#         # Get and assert the feature column names
#         features = numeric_train_df.columns.drop(self.target)
#         if len(features) < 1: raise ValueError("The list of features automatically generated is NULL. Halting. ")
# #        assert (isinstance(self.features, (list, tuple, pd.core.indexes.base.Index))),"'features' must be a list of column names."        
#         # You can use `pd.Series.drop()` to drop a value.
#         #lr = linear_model.LinearRegression()
#         self.lr.fit(self.train_df[features], self.train_df[self.target])
#         self.predictions = self.lr.predict(self.test_df[features])
#         self.mse = mean_squared_error(self.test_df[self.target], self.predictions)
#         self.rmse = np.sqrt(self.mse)
#  
#         return self.rmse
#===============================================================================

    def _roll_inplace(self, df, features, target):
        """
        sets the self.parameters to whats passed in, and then returns the parameters for local use
        """
        self.df = df
        df = self.df
        #
        self.features = features
        features = self.features
        for col in self. target:
            if col not in self.features: print("_roll_inplace:Its not here")
        #
        self.target = target
        target = self.target
        
        return self.df, self.features, self.target
                
    def _train_and_test(self, train_df, test_df):
#         if set(train_df.columns) != set(test_df.columns):
#             raise ValueError("The column lists between train and test columns must match.")
#         self.features = features = test_df.columns.to_list() # Use test_df because it will have the target columns        
#===============================================================================
#         numeric_columns = self.numeric_columns(train_df)
#         # Train must have the target columns
#         numeric_train_df = train_df[numeric_columns]
#         # Test must NOT have the target columns        
#         numeric_test_df  = test_df[set(numeric_columns) - set(self.target)]
# #         numeric_test_df  = test_df[numeric_columns]
#         print("numeric_train_df=", numeric_train_df.shape) #3333
#         print("numeric_test_df=", numeric_test_df.shape)#333
#===============================================================================
#         train_features = numeric_train_df.columns.to_list()
#         for col in self.target:
#             try: train_features.remove(col)
#             except ValueError as e: pass
#         if len(features) < 1: raise ValueError("The list of features automatically generated is NULL. Halting. ")
#        assert (isinstance(self.features, (list, tuple, pd.core.indexes.base.Index))),"'features' must be a list of column names."        
        # You can use `pd.Series.drop()` to drop a value.
        #lr = linear_model.LinearRegression()
        self.lr.fit(train_df[self.features], train_df[self.target])
        self.predictions = self.lr.predict(test_df[self.features])
        mse = mean_squared_error(test_df[self.target], self.predictions)
        rmse = np.sqrt(mse)
        return rmse
        
    def _transform_features_vars(self, 
                                 df, 
                                 features, 
                                 drop, 
                                 percent_missing, 
                                 interpolate, 
                                 carry_forward, 
                                 ):
        self.df = df
        df = self.df 

        if features is None: 
            try:features = self.features
            except Exception as e: raise err.FeaturesPropetyNotSetException("Either set the Class object's 'features' parameter, or pass a list of features to this method.")
        assert (isinstance(self.features, (list, tuple, pd.core.indexes.base.Index))),"'features' must be a list of column names."
        
        if drop is None: 
            try:drop = self.target
            except Exception as e: raise err.TargetPropetyNotSetException("Could not set parameter 'drop' to class default.")
        if not isinstance(drop, (list, tuple, pd.core.indexes.base.Index)): drop = [str(drop)]
        
        try: 
            percent_missing = float(percent_missing)
            if percent_missing < 0: raise ValueError # Invalid 
            if percent_missing > 100: raise ValueError # Invalid
            if percent_missing > 1: percent_missing /= 100 # Make into decimal variation
        except ValueError: 
            raise ValueError("Parameter 'percent_missing' must be an integer between 0 and 100, or a float between .0 and .1.")
        
        # Booleans
        self.interpolate = interpolate
        self.carry_forward = carry_forward
        if (interpolate == True) and (carry_forward == True):
            raise RuntimeError("The parameters 'interpolate' and 'carry_forward' are contradictory. Only one can be set to True. ")
        
        return df, features, drop, percent_missing, interpolate, carry_forward 

    def correlations(self, df = None, features = None, correlation_strength = 0.3):
        """
        """
        # Parameters
        self.df = df
        df = self.df
        self.features = features
        # Return to local features list. 
        # Append the target for sorting. 
        features = self.features
        # Build a separate df, transforming categorical columns into nominal codes
        df = corr_df = df[features]
        for col in df.columns:
            if not (df[col].dtype == np.float64 or df[col].dtype == np.int64):
                codes = pd.Categorical(df[col]).codes
                # Create dummy values that can be correlated
                codes = pd.get_dummies(pd.Categorical(df[col]))
                corr_df[col] = codes
            else:
                corr_df[col] = df[col]

        for target in self.target:
            if target not in corr_df.columns:
                corr_df[target] = self.df[target]

        # Build the correlation tables
        corr_df = corr_df.corr()
        sorted_corrs = corr_df.abs().sort_values(by = self.target, ascending = False)
        strong_corrs = sorted_corrs[sorted_corrs >= correlation_strength]
        corrmat = df[strong_corrs.index].corr()
        return corrmat

    def drop_feature(self, feature_list = None):
        """"""
        if feature_list is None: return 
        elif isinstance(feature_list, str): feature_list = [feature_list]
        elif isinstance(feature_list, (tuple, list, pd.core.indexes.base.Index)):             
            for feature in feature_list:
                try: self.features.remove(feature)
                except ValueError as e:
                    log("Feature '{}' does not appear in the current features list. ".format(feature))
            return
        else:
            raise ValueError("regression.feature_list: Value must be a string, or list of strings containing the text name of a column(s) to delete from the existing features.")

    def drop_nan_cols(self):
        newdf = pd.DataFrame()
        for col in self.df.columns.to_list():
            if self.df[col].isnull.sum() == 0:
                newdf[col] = self.df[col]
        self.df = newdf

    def categorical_columns(self, df = None):
        """
        DO NOT use df here to set self.df
        
        We want to be able to puck out the numaric columns, WITHOUT 
        setting the entire self.df to only numeric columns
        
        Instead return the new df which can then be set by the caller
        if so desired. 
        
        "result" is a separate DataFrame entity that what is passed in as "df"
        """
        self.df = df
        df = self.df 
        result = df.select_dtypes(include=['integer', 'float'])
        return list(self.get_categorical(df = df).keys())
            
    def get_categorical(self, df = None, features = None):
        """
        returns a dict of dicts
        result = {colname: {cat.code1:label1, cat.code2:label2}, ... }
        """
        self.df = df
        df = self.df
        
        result = {}
        self.features = features
        df = df[self.features] # Reduce the df to the columns passed in

        numeric = self.numeric_columns(df)
        catcolumns = set(df.columns) - set(numeric)
        for col in catcolumns:
            cats = pd.Categorical(df[col])
            map = dict( zip( cats.codes, df[col] ) )
            result[col] = {"catigorical":cats, "map":map, "value_counts":cats.value_counts()}
        return result
    
    def heatmap(self, corrmat = None, df = None, features = None, correlation_strength = 0.3, *args, **kwargs):
        self.df = df
        df = self.df
        self.features = features

        df = df[self.features]
        
        if corrmat is None: 
            corrmat = self.correlations(df = df, features = features, correlation_strength = correlation_strength)
        fig, ax = plt.subplots(figsize=(10,10))         # Sample figsize in inches
        sns.heatmap(corrmat, ax=ax, *args, **kwargs)
        plt.show()
        
    def interpolate_rows(self, df = None, features = None, method = "mean", drop = []):  
        """
        :NAME:
            regression.interpolate_rows(df = None, features = None)
            
        :DESCRIPTION:
            Parses the numeric columns (only) of the DataFrame, and fills any 
            NULL (NAN) values using the mean of the row. 
            
        :PARAMETERS:
            df = (Pandas DataFrame) A new DataFrame from which to generate the new
                 DataFrame with the interpolated, numeric columns.
                 
                 If passed in, this will overwrite the existing self.df held by the 
                 "regression" Class object.
                 
                 If not passed in (None) then the self.df will be used. 
                 
            features = (list, tuple, pd.core.indexes.base.Index) If passed in, this
                        list of columns will be used as the only features (columns) 
                        which will be interpolated. 
                        
                        The new DataFram object returned will contain ONLY the numeric columns 
                        (with the  interpolated data) from this list. 
            
                        These columns will have to be reintegrated into the original DataFrame 
                        manually if desired.
                    
            method = (String) The method by which the missing data will be interpolated. 
                     Options include: 
                     Mean   = All missing (NULL or NAN) cells will be replaced with the row mean. 
                     Mode   = All missing (NULL or NAN) cells will be replaced with the row mode. 
                     Median = All missing (NULL or NAN) cells will be replaced with the row median. 
                     Carry_forward   
                            = All missing (NULL or NAN) cells will be replaced with the data
                              from the cell immediately to the left of the NULL/NAN cell.
                    DEFAULT: Mean
        
        :RETURNS:
            A new DataFram object containing ONLY the numeric columns with the 
            interpolated data. 
            
            These columns will have to be reintegrated into the original DataFrame 
            manually if desired. 
        """      
        assert (isinstance(method, str)),"regression.interpolate_rows(): 'method' must be  a string containing 'mean', 'mode', 'median', or 'carry_forward'."
        method = method.lower()
        if "carry_forward" in method: raise NotImplementedError("The 'carry_forward' method is not yet implemented. ")
        self.df = df
        df = self.df
        self.features = features
        
        # Roll through as list, in case some columns DO exist
        for col in drop: 
            try: df = df.drop(col, axis = 1)
            except KeyError: continue
                
        numeric_df = self.df[self.numeric_columns(self.df)]

        result = numeric_df.copy()
        for col in numeric_df.columns:
            if "mean"  in method: result[col] = numeric_df[col].fillna(numeric_df[col].mean())
            if "media" in method: result[col] = numeric_df[col].fillna(numeric_df[col].median())
            if "mode"  in method: result[col] = numeric_df[col].fillna(numeric_df[col].mode())
        
        for col in result.columns: 
            self.df[col] = result[col]
        return self.df

    def make_numerical_df(self, categorical = True):
        """"""
        # Firts convert string and categorical columns to numeric
        if categorical: 
            for col in self.df:
                if not (self.df[col].dtype == np.float64 or self.df[col].dtype == np.int64):
                    self._convert_to_dummies(col, force = False)
        # Next, defacto remove all non-numeric
        self.df = self.df[self.numeric_columns(self.df)]
    
    def numeric_columns(self, df = None):
        """
        DO NOT use df here to set self.df
        
        We want to be able to puck out the numaric columns, WITHOUT 
        setting the entire self.df to only numeric columns
        
        Instead return the new df which can then be set by the caller
        if so desired. 
        
        "result" is a separate DataFrame entity that what is passed in as "df"
        """
        self.df = df
        df = self.df 
        result = df.select_dtypes(include=['integer', 'float'])
        return result.columns.to_list()  

    def train_and_test(self, df = None, features = None, target = "SalePrice", 
                       train_percent = .5, k = 0 ):
        """
        :NAME:
        :DESCRIPTION:
        :PARAMETERS:
            train_percent(int, float): Sets the division of how many rows from the DataFrame
                                       are used for training, and how many used for testing. 
                                       
                                       This can be a "float" between 0 and 1 (percentage) or an
                                       "int" indicating the cutoff values (I.e. 1000 means the 
                                       first 1000 rows will be train, and the remainin [1000:]
                                       will be test. 
                                       
                                       DEFAULT: 0.5 
                                
        """
        df, features, target = self._roll_inplace(df, features, target)
        self.k = k
        self.train_percent = train_percent
        if self.k == 0: return self._holdout()
        if self.k == 1: self.k = 2
        if self.k >= 1: return self._cross_validation()
        raise ValueError("regression.train_and_test: The parameter'k' must be float or integer >= 0")
                                
    def transform_features(self, 
                           df = None, 
                           features = None, 
                           drop = None, 
                           percent_missing = .25, 
                           interpolate = False, 
                           carry_forward = False, 
                           ):
        """"""
        df, features, drop, percent_missing, interpolate, carry_forward = self._transform_features_vars(df, features, drop, percent_missing, interpolate, carry_forward)
        
        # Lazy
        if carry_forward is True: 
            raise NotImplementedError("The 'carry_forward' function is not yet implemented. ")
        
        # remove the drop column(s)
        _features = [f for f in features if f not in drop]
            
        # Remove columns with too many missing value
        result = []
        total_rows = self.df.shape[0]
#         print("Cutoff value for rows missing data = ", total_rows * percent_missing) #333
        for col in _features:
#             print(); print(col)
#             print("null rows =", self.df[col].isnull().sum()) #333
#             print("% null rows =", self.df[col].isnull().sum()/total_rows) #333
            if df[col].isnull().sum() < total_rows * percent_missing:
                result.append(col)
            else: 
                print("regressoin.transform_features: Dropping ", col) #333
        
        if self.interpolate is True: 
            self.interpolate_rows(df = df)
        
        self.features = result 
        return result
            
             
if __name__ == "__main__":
    r = regression()
    r.target = "SalePrice"

#===============================================================================
#     for col in r.df.columns:
# #         if not (r.df[col].dtype == np.float64 or r.df[col].dtype == np.int64):
#         r._convert_to_dummies(col, force = True)
#===============================================================================
#     print(r.numeric_columns())

    #=== CATEGORIES tests ======================================================
    # cats = r.get_categorical()
    # for k,v in cats.items():
    #     print()
    #     print(k)
    #     print("------------------------")
    #     print("object=", v["catigorical"])
    #     print("------------------------")
    #     print("map=", v["map"])
    #     print("------------------------")
    #     print("value_counts=", v["value_counts"])
    #===========================================================================

#=== Heatmap tests =============================================================
# #     f = r.numeric_columns()
# #     f = r.categorical_columns()
#     f = r.numeric_columns()
#     r.heatmap(features = f)
    # categorical_features = list(r.get_categorical().keys()) 
    # r.heatmap(features = categorical_features)
#===============================================================================

#===============================================================================
#     print("features = ({}){}".format(len(r.features), id(r.features)))  
#     features = r.features
#     interpolated_features = r.interpolate_rows(drop = r.target)
#     for f in interpolated_features.columns:
#         if f not in features:
#             print("new col = ", f) 
#     
#     print("interpolated features = ({}){}".format(len(r.features), id(r.features)))  
#     features = r.transform_features(
#         drop = ["SalePrice", "PID"], 
#         percent_missing = .2,
#         carry_forward = False, 
#         interpolate = True
#         )
#     print("transformed features = ({}){}".format(len(r.features), id(r.features)))  
# 
#     
# #===============================================================================

    rmse = r.train_and_test(
        train_percent = 1460,
        k = 0
        )
    print("rmse=", rmse)
    
# #    print("({}){}".format(len(r.features), r.features))  
# 
# #    corrmat = r.correlations()
# #    sns.heatmap(corrmat, xticklabels=True, yticklabels=True)
# #     plt.show()
#  
#     print("({}){}".format(len(r.features), type(r.features)))     
#     r.drop_feature(['PID', 'Order', 'Nadaddaddad', "Mo Sold"])
#     print("({}){}".format(len(r.features), type(r.features)))  
# 
#     corrmat = r.correlations()
#     sns.heatmap(corrmat, xticklabels=True, yticklabels=True)
#     plt.show()
#===============================================================================

#===============================================================================
#         for col in r.df.columns:
#             cat = r.df[col].cat.codes
#             print("{}...{}".format(col, cat))
        

