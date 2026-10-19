# Prince Hands-on Lab: Optimize Model Training in Azure Machine Learning

Learn how to move a machine learning model from a **notebook** (experimentation) to a **production-ready training script**, run it as a tracked **command job**, and then optimize it with **hyperparameter tuning** that trains several models **in parallel** on a compute cluster. All of it uses Azure Machine Learning, the Azure CLI and the Python SDK v2.

**Who this is for:** AI engineers and data scientists who want to improve training efficiency, model performance and deployment readiness with MLOps practices.

| | |
|---|---|
| **Time** | About 90 minutes (some of it is waiting for Azure to create compute and run jobs) |
| **Cost** | About US $0.50–$2.00 if you delete everything at the end ([details](docs/01-prerequisites-and-cost.md#cost-to-perform-the-lab)) |
| **Level** | Intermediate |
| **You need** | An Azure subscription where you are **Owner** or **Contributor**, and Chrome or Edge |

---

## Project overview

**Scenario.** You are an AI engineer at a retail company that wants to optimize its machine learning systems. The goal is to speed up training and improve model performance using MLOps practices: experiment efficiently, track every run, tune the training process, and use compute resources wisely. You practise these techniques on a diabetes-prediction dataset (10,000 patients, target column `Diabetic`). The same workflow applies to any model, including product recommendations.

**What you will do**

1. **Provision** a workspace, a compute instance and a compute cluster with one Azure CLI script.
2. **Experiment** in a notebook and train a logistic regression model.
3. **Convert** the notebook into a Python script.
4. **Refactor and test** a production-style script (functions + parameters) in the terminal.
5. **Run the script as a command job**, so every input, output, metric and log is tracked.
6. **Tune hyperparameters** with a sweep job that trains 4 models, 2 at a time in parallel, and picks the best one.
7. **Clean up** so you stop paying.

```
 Cloud Shell                      Azure Machine Learning workspace (mlw-ai300-l<suffix>)
 ───────────                      ───────────────────────────────────────────────────────
 infra/setup.sh  ──creates──►     Compute instance  ci<suffix>   ← you run notebooks + terminal here
                                  Compute cluster   aml-cluster  ← jobs run here (0–2 nodes)
                                  Data assets       diabetes-training, diabetes-data

 Compute instance
   experimentation/train-classification-model.ipynb  ──export──►  .py script
   src/train-model-parameters.py   ──test in terminal──►  Accuracy / AUC
   run-script-as-command-job.ipynb ──submit──►  Command job  ──MLflow──►  params, metrics, ROC curve
   hyperparameter-tuning.ipynb     ──submit──►  Sweep job: reg_rate ∈ {0.01, 0.1, 1, 10}
                                                  4 trials, 2 in parallel on 2 nodes → best model
```

---

## Lab steps

Follow these in order. Every page is click by click.

| # | Step | What you do |
|---|---|---|
| 0 | [Overview and key concepts](docs/00-overview-and-concepts.md) | The ideas behind the lab (5 minutes) |
| 1 | [Prerequisites and cost](docs/01-prerequisites-and-cost.md) | Check your role, set a billing alert, check quota |
| 2 | [Provision the workspace and compute](docs/02-provision-workspace.md) | Run `infra/setup.sh` in Cloud Shell |
| 3 | [Clone the lab materials](docs/03-clone-lab-materials.md) | Open the studio and clone this repo onto your compute instance |
| 4 | [Convert a notebook to a script](docs/04-convert-notebook-to-script.md) | Run the notebook, then export it as `.py` |
| 5 | [Test a script in the terminal](docs/05-test-script-in-terminal.md) | Run the parameterised training script |
| 6 | [Run the script as a command job](docs/06-run-command-job.md) | Submit the job and explore its tracking |
| 7 | [Optimize with hyperparameter tuning](docs/07-hyperparameter-tuning.md) | Run a sweep job and find the best model |
| 8 | [Share your learnings](docs/08-share-your-learnings.md) | Post your result on LinkedIn and in the community |
| 9 | [Delete resources](docs/09-cleanup.md) | **Delete everything so you stop paying** |
| 10 | [Troubleshooting](docs/10-troubleshooting.md) | Fixes for every common error in this lab |

> **Stuck?** Go to [Troubleshooting](docs/10-troubleshooting.md). Each error is listed with the message, the cause and the fix.

---

## Repository layout

```
Azure-Model-training-Optimization/
├── README.md
├── docs/                                   <- the click-by-click lab guide (steps 0-10)
├── infra/
│   ├── setup.sh                            <- creates workspace, compute and data assets
│   └── cleanup.sh                          <- deletes everything
├── data/diabetes-data/                     <- training data (diabetes.csv + MLTable)
├── experimentation/
│   ├── train-classification-model.ipynb    <- step 4: experimentation notebook
│   ├── run-script-as-command-job.ipynb     <- step 6: command job
│   ├── hyperparameter-tuning.ipynb         <- step 7: sweep job
│   ├── lab_helpers.py                      <- workspace connection + environment picker
│   └── environment/conda.yml               <- fallback training environment
└── src/
    └── train-model-parameters.py           <- step 5: production training script
```

## Documentation links

- Azure Machine Learning: https://azure.microsoft.com/en-us/products/machine-learning
- What is Azure Machine Learning? https://learn.microsoft.com/en-us/azure/machine-learning/overview-what-is-azure-machine-learning?view=azureml-api-2
- Azure Machine Learning documentation: https://learn.microsoft.com/en-us/azure/machine-learning/?view=azureml-api-2
- Command jobs: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-train-model?view=azureml-api-2
- Hyperparameter tuning (sweep jobs): https://learn.microsoft.com/en-us/azure/machine-learning/how-to-tune-hyperparameters?view=azureml-api-2
- MLflow tracking: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-mlflow-configure-tracking?view=azureml-api-2

## Summary

In this lab you:

- **Set up an Azure Machine Learning workspace** and compute with a repeatable CLI script.
- **Moved from notebook to script**: exported the experiment, then used a function-based, parameterised script.
- **Tracked experiments** by running the script as a command job, with MLflow logging parameters, metrics and the ROC curve.
- **Implemented hyperparameter tuning** with a sweep job that compared regularization rates automatically.
- **Used multiple compute resources** by running trials in parallel across the cluster's two nodes, cutting total tuning time roughly in half.
- **Cleaned up resources** to avoid unnecessary costs.

---

*Prince Hands-on Labs. Based on Microsoft Learn's open-source MLOps lab ([MicrosoftLearning/mslearn-mlops](https://github.com/MicrosoftLearning/mslearn-mlops)), updated and fixed for classroom use.*
