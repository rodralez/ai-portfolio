import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import LassoCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_absolute_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt

def model_performance (y_test, y_pred):

    # Calculate MSE
    mae = mean_absolute_error(y_true=y_test, y_pred=y_pred)

    # Calculate R^2 (coefficient of determination) regression score function
    r2 = r2_score(y_true=y_test, y_pred=y_pred)

    return mae, r2

def data_splitting (data, target):
    
    test_size = 0.2

    # Divide the dataframe into training and testing samples
    train_X, test_X = train_test_split(data, test_size=test_size)

    X_train = train_X.drop([target] , axis=1)
    y_train = train_X[target]
    X_test = test_X.drop([target] , axis=1)
    y_test = test_X[target]

    return X_train, y_train, X_test, y_test

def linear_regressor (X_train, y_train, X_test, cv=10):
            
    # lr = ElasticNetCV(l1_ratio=np.arange(0.1, 1, 0.1), alphas=np.arange(0.1, 100, 0.5), cv=cv)
    lr = ElasticNetCV(cv=cv)
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)

    return y_pred, lr 

def linear_regressor_cv (data, feat_drop, feat_target, CV=10, cv=10):
            
    # drop 
    data = data.drop([feat_drop] , axis=1)

    y_pred_l = np.empty((0, ), dtype=float)
    y_test_l = []
    lr_models_l = []
    mae_l = []
    r2_l = []
    mae_bl_l = []
    r2_bl_l = []
    coeff_l = []
    intercept_l = []
    l1_ratio_l = []
    alpha_l = []

    # Baseline performance
    mean_target = data[feat_target].mean()

    for i in range(CV) :

        # split data randomly
        X_train, y_train, X_test, y_test = data_splitting (data, target=feat_target)

        # glmnet predictor
        regr = ElasticNetCV(l1_ratio=np.arange(0.1, 1, 0.1), alphas=np.arange(0.1, 10, 0.5), cv=cv)
        # regr = ElasticNetCV(cv=cv)
        regr.fit(X_train, y_train)
        y_pred = regr.predict(X_test)

        # save the model parameters
        coeff_l.append(regr.coef_)  
        intercept_l.append(regr.intercept_)  
        l1_ratio_l.append(regr.l1_ratio_) 
        alpha_l.append(regr.alpha_) 

        # save the model
        lr_models_l.append(('gmlnet_%d' % i, regr))

        # save y_pred and y_test
        y_pred_l = np.concatenate((y_pred_l, y_pred)) 
        y_test_l = np.concatenate((y_test_l, y_test)) 

        # save model performance
        mae, r2 = model_performance (y_test, y_pred)
        mae_l.append(mae) 
        r2_l.append(r2)

        # save baseline performance
        
        mean_bl = np.full_like(y_test, mean_target)
        mae_bl, r2_bl = model_performance (y_test, mean_bl)
        mae_bl_l.append(mae_bl) 
        r2_bl_l.append(r2_bl)

    return (lr_models_l, coeff_l, intercept_l, l1_ratio_l, 
            alpha_l, mae_bl_l, r2_bl_l, mae_l, r2_l, y_pred_l, y_test_l)


def lasso_regressor (X_train, y_train, X_test, cv=False, scale=False):

    if (scale == True) :            
        scaler = StandardScaler()
        scaler.fit(X_train)
        
        # scale the selected columns using the scaler and store the result in 
        # a new DataFrame
        X_s1 = scaler.transform(X_train)
        X_train = pd.DataFrame(data=X_s1, columns=X_train.columns)
        X_s2 = scaler.transform(X_test)
        X_test = pd.DataFrame(data=X_s2, columns=X_train.columns)

    if (cv == True) :
        lassocv = LassoCV(cv=10)
        lassocv = lassocv.fit(X_train, y_train)
        y_pred = lassocv.predict(X_test)

        return y_pred, lassocv 

    else :

        lasso = Lasso()
        lasso = lasso.fit(X_train, y_train)
        y_pred = lasso.predict(X_test)

        return y_pred, lasso

def color_palette() :

    # Create custom color palette
    clr_palette = sns.color_palette("YlOrBr", n_colors=6)
    clr_palette[0] = "#fee391" 
    clr_palette[1] = "#fec44f" 
    clr_palette[2] = "#fe9929" 
    clr_palette[3] = "#d95f0e" 
    clr_palette[4] = "#993404" 
    clr_palette[5] = "#000000" 

    return clr_palette

def my_regplot(data, x, y, title, xlabel, ylabel, hue=None, pallete="flare") :

    sns.set()
    sns.set_theme(style='white')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x=x, y=y, data=data, scatter=False, color='lightgreen', ci=0)
    sns.scatterplot(x=x, y=y, data=data, hue=hue, s=100, palette=pallete)
    plt.title(title, fontsize=20)
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.grid(axis='y')
    # plt.grid()
    plt.show()

def my_waste_regplot(data, x, y, title, xlabel, ylabel, hue=None) :

    sns.set()
    sns.set_theme(style='white')
    fig, ax = plt.subplots(figsize=(8, 6))
    # sns.regplot(x=x, y=y, data=data, scatter=False, color='lightgreen', ci=0)
    sns.scatterplot(x=x, y=y, data=data, hue=hue, s=100, palette=sns.color_palette("flare", as_cmap=True))
    plt.title(title, fontsize=20)
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    ax.grid(axis='y')
    # plt.grid()
    plt.show()

def my_barplot(data, x, y, palette=None) :

    sns.set()
    sns.set_theme(style='white')
    # Create a boxplot using seaborn
    ax=sns.barplot(y=y, x=x, data=data, palette=palette, orient='h', errorbar=None)
    ax.grid(axis='x')
    plt.xlabel(x, fontsize=20)
    plt.ylabel(y, fontsize=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()

def whatif_analysis(data, weights, intercept, feature_fixed, 
                    feature_fixed_value, target_fixed_value) :

    # consider the mean for the rest of the parameters, except for the fixed parameter
    x_mean = data.mean() 
    x_mean[feature_fixed] = feature_fixed_value

    # preallocate what-if features dataframe
    whatif_features = pd.DataFrame(data = np.zeros( np.size(x_mean) ) ,
                                    index = x_mean.index , 
                                    columns = ['values'])

    for feature in x_mean.index :

        w = weights.drop([feature])
        xm = x_mean.drop([feature])
        w_feat = weights['weight'][feature]
            
        if (w_feat != 0) :
            whatif_features['values'][feature] = (target_fixed_value - intercept - np.dot(xm , w)) / w_feat

    target_test = intercept + np.dot(x_mean, weights)

    return whatif_features, target_test
