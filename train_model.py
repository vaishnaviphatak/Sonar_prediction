import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

def train_and_save_model():
    print("Loading data...")
    # Read the data file
    sonar_data = pd.read_csv('Copy of sonar data.csv', header=None)

    print("Data loaded successfully. Splitting data...")
    # Separate data and labels
    X = sonar_data.drop(columns=60, axis=1)
    Y = sonar_data[60]

    # Split into training and testing data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, stratify=Y, random_state=1)

    print("Training Logistic Regression model...")
    # Initialize and train model
    model = LogisticRegression()
    model.fit(X_train, Y_train)

    # Evaluate model
    X_train_prediction = model.predict(X_train)
    training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
    print(f"Accuracy on training data: {training_data_accuracy}")

    X_test_prediction = model.predict(X_test)
    test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
    print(f"Accuracy on test data: {test_data_accuracy}")

    print("Saving model to model.pkl...")
    # Save the trained model
    joblib.dump(model, 'model.pkl')
    print("Model saved successfully!")

if __name__ == '__main__':
    train_and_save_model()
