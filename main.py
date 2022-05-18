from sklearn.model_selection import train_test_split
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from flask import jsonify
import numpy as np
import pandas as pd
import feature_extraction


def getResult(url):

    #Importing dataset
    data = np.loadtxt("phishing.csv", delimiter = ",")

    #Seperating features and labels
    X = data[: , :-1]
    y = data[: , -1]

    #Seperating training features, testing features, training labels & testing labels
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    clf = RandomForestClassifier(max_depth=32, random_state=0)
    clf = clf.fit(X_train, Y_train)
    Y_prediction = clf.predict(X_test)

    from sklearn.model_selection import ShuffleSplit

    cv = ShuffleSplit(n_splits=5, test_size=0.2)

    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(clf, X, Y, cv=cv)
    print("Cross fold validation accuracy mean:", scores.mean())

    X_new = []

    X_input = url
    X_new=feature_extraction.generate_data_set(X_input)
    X_new = np.array(X_new).reshape(1,-1)

    try:
        prediction = clf.predict(X_new)
        if prediction == -1:
            return "Phishing Url"
        else:
            return "Legitimate Url"
    except:
        return "Phishing Url"