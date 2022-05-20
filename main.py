import numpy as np
import feature_extraction
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.model_selection import train_test_split
from flask import jsonify


def getResult(url):

    #Dataset is imported using numpy
    data = np.loadtxt("phishing.csv", delimiter = ",")

    #Seperating features and labels
    X = data[: , 0:14]
    y = data[: , 15]


    #Making the training and testing features and labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    #Setting random forest features
    clf = rfc(max_depth=32, random_state=0)
    clf.fit(X_train, y_train)
    Y_prediction = clf.predict(X_test)

    from sklearn.model_selection import ShuffleSplit

    cv = ShuffleSplit(n_splits=5, test_size=0.2)

    # Produces accuracy score of the algorithm using cross fold validation
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(clf, X, y, cv=cv)
    print("Accuracy score", scores.mean())

    X_new = []

    X_input = url
    X_new=feature_extraction.generate_data_set(X_input)
    X_new = np.array(X_new).reshape(1,-1)

    #Determines whether the URL entered is phishing or legitmate
    try:
        prediction = clf.predict(X_new)
        if prediction == 1:
            return "Phishing Url"
        else:
            return "Legitimate Url"
    except:
        return "Phishing Url"
