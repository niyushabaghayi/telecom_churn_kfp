import kfp
from kfp import dsl
from kfp.components import func_to_container_op

@func_to_container_op
def show_results(ada_boost : float, logistic_regression : float, random_forest : float, svm : float, xg_boost : float) -> None:
    # Given the outputs from decision_tree and logistic regression components
    # the results are shown.

    print(f"Ada Boost (accuracy): {ada_boost}")
    print(f"Logistic regression (accuracy): {logistic_regression}")
    print(f"Random Forest (accuracy): {random_forest}")
    print(f"SVM (accuracy): {svm}")
    print(f"XG Boost (accuracy): {xg_boost}")


@dsl.pipeline(name="Telecom Churn Prediction", description="Applies Several Models for classification problem.")
def telecom_pipeline():

    # Loads the yaml manifest for each component
    ingestion = kfp.components.load_component_from_file("ingestion/ingestion.yaml")
    preprocess = kfp.components.load_component_from_file("preprocess/preprocess.yaml")
    ada_boost = kfp.components.load_component_from_file("ada_boost/ada_boost.yaml")
    logistic_regression = kfp.components.load_component_from_file("logistic_regression/logistic_regression.yaml")
    random_forest = kfp.components.load_component_from_file("random_forest/random_forest.yaml")
    svm = kfp.components.load_component_from_file("svm/svm.yaml")
    xg_boost = kfp.components.load_component_from_file("xg_boost/xg_boost.yaml")

    # Run ingestion task
    ingestion_task = ingestion()

    # Run preprocess task
    preprocess_task = preprocess(ingestion_task.output)

    # Run tasks Models given
    # the output generated by "ingestion_task".
    ada_boost_task = ada_boost(preprocess_task.output)
    logistic_regression_task = logistic_regression(preprocess_task.output)
    random_forest_task = random_forest(preprocess_task.output)
    svm_task = svm(preprocess_task.output)
    xg_boost_task = xg_boost(preprocess_task.output)

    # Given the outputs from "decision_tree" and "logistic_regression"
    # the component "show_results" is called to print the results.
    show_results(ada_boost_task.output, logistic_regression_task.output, random_forest_task.output, svm_task.output, xg_boost_task.output)



if __name__ == "__main__":
    kfp.compiler.Compiler().compile(telecom_pipeline, "TelecomChurn.yaml")
    # kfp.Client().create_run_from_pipeline_func(basic_pipeline, arguments={})