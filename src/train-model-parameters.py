# Prince Hands-on Lab - Optimize model training in Azure Machine Learning
#
# Production-style training script: the code from the experimentation notebook,
# organised into functions and parameterised with command-line arguments.
#
# Run it in a terminal (from the src folder):
#     python train-model-parameters.py --training_data ../data/diabetes-data/diabetes.csv
#     python train-model-parameters.py --training_data ../data/diabetes-data --reg_rate 0.1
#
# When it runs as an Azure Machine Learning job, it also logs the parameter,
# metrics and ROC curve with MLflow so you can compare runs in the studio.

import argparse
import glob
import os

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split

FEATURES = ['Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure', 'TricepsThickness',
            'SerumInsulin', 'BMI', 'DiabetesPedigree', 'Age']
TARGET = 'Diabetic'

# MLflow logging only happens inside an Azure ML job. In a plain terminal the
# script still runs, even if mlflow isn't installed or configured there.
IN_AZUREML_JOB = bool(os.environ.get("AZUREML_RUN_ID") or os.environ.get("MLFLOW_RUN_ID"))
mlflow = None
if IN_AZUREML_JOB:
    try:
        import mlflow  # noqa: F811
    except ImportError:
        print("mlflow is not installed in this environment - metrics will only be printed.")
        mlflow = None


def log_param(name, value):
    if mlflow:
        mlflow.log_param(name, value)


def log_metric(name, value):
    if mlflow:
        mlflow.log_metric(name, value)


def main(args):
    # read data
    df = get_data(args.training_data)

    # split data
    X_train, X_test, y_train, y_test = split_data(df)

    # train model
    model = train_model(args.reg_rate, X_train, X_test, y_train, y_test)

    # evaluate model
    eval_model(model, X_test, y_test)


# function that reads the data from a CSV file, or from a folder of CSV files
def get_data(path):
    print("Reading data...")
    if not path:
        raise SystemExit("ERROR: no training data given. Add --training_data <path to csv or folder>, e.g.\n"
                         "    python train-model-parameters.py --training_data ../data/diabetes-data/diabetes.csv")
    if os.path.isdir(path):
        csv_files = sorted(glob.glob(os.path.join(path, "*.csv")))
        if not csv_files:
            raise SystemExit(f"ERROR: no CSV files found in folder: {path}")
        df = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)
    elif os.path.isfile(path):
        df = pd.read_csv(path)
    else:
        raise SystemExit(f"ERROR: training data path not found: {path}\n"
                         f"Current folder is {os.getcwd()} - check the relative path.")
    print(f"Read {len(df):,} rows")
    return df


# function that splits the data
def split_data(df):
    print("Splitting data...")
    X, y = df[FEATURES].values, df[TARGET].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)
    return X_train, X_test, y_train, y_test


# function that trains the model
def train_model(reg_rate, X_train, X_test, y_train, y_test):
    log_param("Regularization rate", reg_rate)
    print(f"Training model (regularization rate {reg_rate})...")
    model = LogisticRegression(C=1 / reg_rate, solver="liblinear").fit(X_train, y_train)
    return model


# function that evaluates the model
def eval_model(model, X_test, y_test):
    # calculate accuracy
    y_hat = model.predict(X_test)
    acc = np.average(y_hat == y_test)
    print('Accuracy:', acc)
    log_metric("Accuracy", acc)

    # calculate AUC
    y_scores = model.predict_proba(X_test)
    auc = roc_auc_score(y_test, y_scores[:, 1])
    print('AUC: ' + str(auc))
    log_metric("AUC", auc)

    # plot ROC curve (skipped if matplotlib isn't available)
    try:
        import matplotlib
        matplotlib.use("Agg")  # no screen needed
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed - skipping ROC curve plot.")
        return
    fpr, tpr, thresholds = roc_curve(y_test, y_scores[:, 1])
    plt.figure(figsize=(6, 4))
    plt.plot([0, 1], [0, 1], 'k--')  # diagonal 50% line
    plt.plot(fpr, tpr)               # FPR and TPR achieved by the model
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.savefig("ROC-Curve.png")
    plt.close()
    if mlflow:
        mlflow.log_artifact("ROC-Curve.png")


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data', type=str)
    parser.add_argument("--reg_rate", dest='reg_rate', type=float, default=0.01)

    # parse args
    return parser.parse_args()


# run script
if __name__ == "__main__":
    print("\n\n")
    print("*" * 60)

    args = parse_args()
    main(args)

    print("*" * 60)
    print("\n\n")
