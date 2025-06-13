from src.logging.logger import logger
from src.exception.exception import NetworkSecurityException
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from src.utils.utils import save_object, load_object, load_numpy_array_data
from src.utils.ml_utils.utils import get_classification_score, evaluate_models
from src.utils.ml_utils.estimator import NetworkModel
import os, sys
import mlflow
from dotenv import load_dotenv
load_dotenv()

os.environ["MLFLOW_TRACKING_URI"]= os.getenv('MLFLOW_TRACKING_URI')
os.environ["MLFLOW_TRACKING_USERNAME"]= os.getenv('MLFLOW_TRACKING_USERNAME')
os.environ["MLFLOW_TRACKING_PASSWORD"]= os.getenv('MLFLOW_TRACKING_PASSWORD')


mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
# mlflow.set_tracking_username(os.getenv("MLFLOW_TRACKING_USERNAME"))
# mlflow.set_tracking_password(os.getenv("MLFLOW_TRACKING_PASSWORD"))

import dagshub
dagshub.init(repo_owner='jayawinata100', repo_name='Network-Security-System', mlflow=True)

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_model(self, best_model, classification_metric, best_model_name):
        try:
            with mlflow.start_run():
                f1_score = classification_metric.f1_score
                precision_score = classification_metric.precision_score
                recall_score = classification_metric.recall_score

                mlflow.log_metrics({
                    'f1_score': f1_score,
                    'precision_score': precision_score,
                    'recall_score': recall_score
                })
                mlflow.sklearn.log_model(best_model, best_model_name)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Logistic Regression": LogisticRegression(verbose=1),
            "K-Nearest Neighbor": KNeighborsClassifier()
        }

        params = {
            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
            },
            "Random Forest": {
                'n_estimators': [8,16,32,64]
            },
            "Logistic Regression": {},
            "K-Nearest Neighbor": {}
        }

        model_report = evaluate_models(X_train, y_train, X_test, y_test, models = models, params = params)
        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(y_train, y_train_pred)

        # Mlflow Tracking
        self.track_model(best_model, classification_train_metric, best_model_name)

        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_score(y_test, y_test_pred)

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, obj=network_model)
        save_object('final_model/model.pkl', best_model)

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )

        logger.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact


    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            model_trainer_artifact = self.train_model(X_train, y_train, X_test, y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)