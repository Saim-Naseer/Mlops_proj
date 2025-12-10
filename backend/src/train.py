import pandas as pd
import numpy as np
import pickle
import yaml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LassoCV, Lasso, RidgeCV, Ridge, ElasticNetCV, ElasticNet
from sklearn.metrics import r2_score
import mlflow
import mlflow.sklearn

with open("params.yml", "r") as f:
    params = yaml.safe_load(f)

train_params = params["train"]
preprocess_params = params["preprocess"]
paths = params["paths"]
mlflow_params = params["mlflow"]

df = pd.read_csv("data/processed.csv")
x = df.drop(columns=["y"])
y = df["y"]

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=preprocess_params["test_size"],
    random_state=preprocess_params["random_state"]
)

def adjr2_score(model, X, y):
    r2 = model.score(X, y)
    n = X.shape[0]
    p = X.shape[1]
    return 1 - (1 - r2) * (n - 1) / (n - p - 1)

mlflow.set_tracking_uri(mlflow_params["tracking_uri"])
mlflow.set_experiment(mlflow_params["experiment_name"])

with mlflow.start_run():

    models = {}

    # Linear Regression
    linear = LinearRegression()
    linear.fit(x_train, y_train)
    models["Linear"] = linear

    # Lasso
    lassocv = LassoCV(alphas=None, cv=50, max_iter=20000000)
    lassocv.fit(x_train, y_train)
    lasso_lr = Lasso(alpha=lassocv.alpha_)
    lasso_lr.fit(x_train, y_train)
    models["Lasso"] = lasso_lr

    # Ridge
    ridgecv = RidgeCV(alphas=np.random.uniform(0,10,50), cv=15)
    ridgecv.fit(x_train, y_train)
    ridge_lr = Ridge(alpha=ridgecv.alpha_)
    ridge_lr.fit(x_train, y_train)
    models["Ridge"] = ridge_lr

    # ElasticNet
    elasticcv = ElasticNetCV(alphas=None, cv=10)
    elasticcv.fit(x_train, y_train)
    elastic_lr = ElasticNet(alpha=elasticcv.alpha_, l1_ratio=elasticcv.l1_ratio_)
    elastic_lr.fit(x_train, y_train)
    models["ElasticNet"] = elastic_lr

    # Evaluate all models and log metrics
    metrics_dict = {}
    for name, model in models.items():
        r2 = model.score(x_test, y_test)
        adj_r2 = adjr2_score(model, x_test, y_test)
        metrics_dict[name] = {"r2": r2, "adj_r2": adj_r2}
        mlflow.log_metric(f"{name}_r2", r2)
        mlflow.log_metric(f"{name}_adj_r2", adj_r2)

    best_model = ridge_lr
    pickle.dump(best_model, open(paths["model_out"], "wb"))
    mlflow.sklearn.log_model(best_model, "ridge_model", registered_model_name="RidgeRegressionModel")

print("Training complete. Metrics:", metrics_dict)