from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor

from sklearn.linear_model import LogisticRegression

from sklearn.svm import LinearSVC
from sklearn.svm import LinearSVR

from sklearn.neural_network import MLPRegressor
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier
from xgboost import XGBRegressor

from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import VotingRegressor

from sklearn.metrics import roc_curve
from sklearn.metrics import mean_squared_error
from sklearn import metrics
import numpy as np
import io
from sklearn import preprocessing
import pandas

import warnings
warnings.filterwarnings("ignore")

def _auc(model):
    y_pred_rf = model.predict_proba(xte)[:, 1]
    fpr_rf, tpr_rf, _ = roc_curve(yte, y_pred_rf)
    result = metrics.auc(fpr_rf,tpr_rf)
    return result

def _classify():
    #------------Classification------------

    #knn
    n = 1
    bestAUC = float('-inf')
    bestModel = None
    count = 2
    while True:
        print('training knn with '+str(n)+' neighbors')
        knnc = KNeighborsClassifier(n_neighbors=n)
        knnc.fit(xtr,ytr)
        currAUC = _auc(knnc)

        if currAUC-bestAUC < 0.05:
            if count <= 0 :
                if currAUC < bestAUC:
                    knnc = bestModel
                break
            else:
                count -= 1
                if currAUC > bestAUC:
                    bestModel = knnc
                    bestAUC = currAUC
                n += 5

        else:
            bestModel = knnc
            bestAUC = currAUC
            n += 5
            count = 2


    #logistic
    bestAUC = float('-inf')
    bestModel = None
    c = 0.0001
    count = 2
    while True:
        print('training logistic regression with c='+str(c))
        lr = LogisticRegression(C = c)
        lr.fit(xtr,ytr)
        currAUC = _auc(lr)

        if currAUC-bestAUC < 0.05:
            if count <= 0 :
                if currAUC < bestAUC:
                    lr = bestModel
                break
            else:
                count -= 1
                if currAUC > bestAUC:
                    bestModel = lr
                    bestAUC = currAUC

                c *= 10
        else:
            bestModel = lr
            bestAUC = currAUC
            c *= 10
            count = 2

    #nn
    print('creating NN classifier')
    mlpc = MLPClassifier()

    #xgboost
    d = 1
    bestAUC = float('-inf')
    bestModel = None
    count = 2
    while True:
        print('training xgboost with '+str(d)+' depth')
        xgbc = XGBClassifier(max_depth=d)
        xgbc.fit(xtr,ytr)
        currAUC = _auc(xgbc)

        if currAUC-bestAUC < 0.05:
            if count <= 0 :
                if currAUC < bestAUC:
                    xgbc = bestModel
                break
            else:
                count -= 1
                if currAUC > bestAUC:
                    bestModel = xgbc
                    bestAUC = currAUC
                d += 5

        else:
            bestModel = xgbc
            bestAUC = currAUC
            d += 5
            count = 2



    #voting
    #generate powersets of estimators
    estimators=[('knnc', knnc), ('lr', lr), ('mlpr', mlpc), ('xgbr', xgbc)]
    votes = [[]]
    for v in estimators:
        votes += [item+[v] for item in votes]
    votes.remove([])

    #train and test each voting classifier
    AUCDict = dict()
    AUCList = []
    for combo in votes:
        print("training voting classifier of "+str([c[0] for c in combo]))
        votec = VotingClassifier(estimators=combo, voting='soft')
        votec = votec.fit(xtr, ytr)
        AUCDict[tuple(combo)] = _auc(votec)
        AUCList.append(tuple(combo))

    AUCList.sort(key=lambda x: -AUCDict[x])
    for s in AUCList:
        print(AUCDict[s])
        print(s)
        print()

def _regress():
    #------------Regression------------

    #knn
    knnr = KNeighborsRegressor()
    #logistic
    lr = LogisticRegression()
    #svm
    svr = LinearSVR()
    #nn
    mlpr = MLPRegressor()
    #xgboost
    xgbr = XGBRegressor()
    #voting
    votec = VotingRegressor(estimators=[
         ('knnr', knnr), ('lr', lr), ('svr', svr), ('mlpr', mlpr), ('xgbr', xgbr)])
    votec = votec.fit(xtr, ytr_encoded)

    y_pred = votec.predict(xte)
    print()
    print(mean_squared_error(y_true = yte, y_pred = y_pred))
    print()



if __name__ == "__main__":

    file_name = input("Enter file name: ")
    id = input("Enter save id: ")
    shuffle = input("Enter 1 for shuffle or 0 for no shuffle: ")
    classify = input("Enter 1 for classify or 0 for regression (default = 0): ")
    ratio = input("Enter percent of test data (default = 0.25): ")

    if shuffle == '1':
        shuffle = 1
    elif shuffle == '0':
        shuffle = 0
    else:
        raise ValueError("Invalid shuffle value entered.")

    if classify == '1':
        classify = 1
    elif classify == '0' or classify == '':
        classify = 0
    else:
        raise ValueError("Invalid classify value entered.")

    if ratio == '':
        ratio = 0.25
    else:
        ratio = float(ratio)

        if ratio <= 0 or ratio >=1:
            raise ValueError("Invalid ratio value entered.")

    # with io.open(file_name, 'r', encoding='UTF-16') as f:
    #     data = np.genfromtxt(f)

    data = pandas.read_csv(file_name).to_numpy()

    #convert cateogries to numbers
    le = preprocessing.LabelEncoder()
    for i in range(data.shape[1]):
        data[:,i] = le.fit_transform(data[:,i])

    data = data.astype(float)

    #shuffle
    if shuffle:
        np.random.shuffle(data)

    X = data[:,:-1]
    Y = data[:,-1]

    xte = X[-int(len(X)*ratio):,]
    yte = Y[-int(len(Y)*ratio):,]
    xtr = X[:-int(len(X)*ratio),]
    ytr = Y[:-int(len(Y)*ratio),]

    lab_enc = preprocessing.LabelEncoder()
    ytr_encoded = lab_enc.fit_transform(ytr)

    if classify:
        # for i in range(len(Y)):
        #     if Y[i]>0:
        #         Y[i] = 1
        #     else:
        #         Y[i] = 0
        _classify()
    else:
        _regress()
