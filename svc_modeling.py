from sklearn.cross_validation import cross_val_score
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.grid_search import GridSearchCV
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from atty_interactions import make_atty_interactions_df
import sys

def test_model(model, param_grid, scale = True, model_spec_function = 'Identity'):
    '''
    Function for grid search optimization of hyperparameters.

    Args:
        model - sklearn model
        param_grid - dictionary of hyperparameters for grid search
        scale - Boolean indicating if the X_train should be scaled using standard scaler. Use for regularized linear models (SVC, log reg)
        model_spec_function- Optional argument. If none passed, default is test_model will load the train.csv data. Otherwise, you can pass a model specification function that take as arugments the filepath and returns X_train, y_train dataframe.

    Returns:
        grid - the fit, scored GridSearchCV object
    '''

    if model_spec_function == 'Identity':
        print 'Reading training data train.csv'

        train_data = pd.read_csv('./../data/final_data/train.csv')

        x_cols = np.setdiff1d(train_data.columns, ['appl_dec_G', 'appl_dec_D', 'appl_dec_F', 'appl_dec_L'])

        X_train = train_data[x_cols]
        y_train = train_data['appl_dec_G']

    else:
        print 'Reading training data train.csv and making design matrix using {}'.format(model_spec_function.__name__)
        X_train, y_train = model_spec_function('./../data/final_data/train.csv')

    if scale == True:
        print 'Scaling features'

        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train_scaled = scaler.transform(X_train)

    elif scale == False:
        X_train_scaled = X_train

    print 'Conducting grid search'
    np.random.seed(4590385)
    grid = GridSearchCV(model(), param_grid=param_grid, scoring='roc_auc',cv=5,n_jobs = -1, pre_dispatch = '2*n_jobs')
    grid.fit(X_train_scaled, y_train)

    return grid

if __name__ == '__main__':

    ### This is for my svc_model
    model = LinearSVC
    Cs = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
    param_grid = {'C': Cs}

    """
    First SVC Model:

    grid = test_model(model, param_grid, scale = True)
    output = open('svc1.pkl','wb')
    pickle.dump(grid, output)
    output.close()
    """
    """
    Second SVC Model:
    """

    ##Needed for atty_interactions generation using Patsy
    sys.setrecursionlimit(5000)

    grid = test_model(model, param_grid, scale = True, model_spec_function = make_atty_interactions_df)

    output = open('svc1_atty_interactions.pkl','wb')
    pickle.dump(grid, output)
    output.close()