import mlflow
from mlflow.models import infer_signature

mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

mlflow.set_experiment("Heart Disease Prediction Project")

with mlflow.start_run():
    mlflow.log_params(rf_params)

    mlflow.log_metric("root_mean_squared_error", rf_rm2e)
    mlflow.log_metric("mean_absolute_error", rf_mae)
    mlflow.log_metric("Accuracy", rf_acc_score*100)

    mlflow.set_tag("Training Info", "Random Forest for Heart Disease Prediction,n_estimators=70")

    signature = infer_signature(X_train, rff.predict(X_train))

    model_info = mlflow.sklearn.log_model(
        sk_model=rff,
        artifact_path="heart_disease_prediction_model",
        signature=signature,
        input_example=preprocessor.transform(X_train),
        registered_model_name="random_forest_model_n_estimators=70",
    )