# Step 0 – Overview and key concepts

[⬅ Back to README](../README.md) | [Next: Prerequisites and cost ➡](01-prerequisites-and-cost.md)

## Introduction

As machine learning models get more complex, training takes longer and uses more resources. This lab shows the MLOps practices that keep training efficient:

- **Scripts instead of notebooks for production.** Notebooks are great for exploring; scripts are repeatable, testable and automatable.
- **Parameters instead of hard-coded values.** The same script can train on new data or with new settings without editing the code.
- **Tracked jobs.** Every run's inputs, code, metrics and logs are stored, so you can compare runs and reproduce them.
- **Hyperparameter tuning.** Let Azure try several settings and pick the best model automatically.
- **Using compute efficiently.** Run trials in parallel on a cluster that scales to zero when idle, so you only pay while training.

## Key concepts

### Azure portal
The web interface for managing Azure resources (https://portal.azure.com). You use it to open Cloud Shell, check resources and delete them at the end. It supports role-based access control (RBAC), which decides who can do what.

### Azure Machine Learning workspace
The central hub for machine learning on Azure. It stores your data assets, environments, jobs, metrics and models, and manages your compute. You work with it through the **studio** (https://ml.azure.com), the **Azure CLI** and the **Python SDK**.

### Azure CLI
A command-line tool for managing Azure. With the `ml` extension it can create workspaces, compute and data assets. In this lab, `infra/setup.sh` uses it to build everything in one go. That's how production teams make infrastructure repeatable.

### Python SDK (azure-ai-ml, v2)
The Python library for Azure Machine Learning. The notebooks use it to connect to the workspace and submit command and sweep jobs.

### Compute instance vs compute cluster
| | Compute instance (`ci<suffix>`) | Compute cluster (`aml-cluster`) |
|---|---|---|
| What | One personal VM | A pool of 0–2 VMs |
| Used for | Notebooks, terminal, development | Running jobs |
| Billing | **Every hour it is running.** Stop it when you're not using it. It auto-stops after 60 idle minutes. | Only while jobs run. It scales down to 0 nodes when idle. |

### Command job
Runs a script on a compute target and records everything: the code snapshot, inputs, environment, logs, metrics and outputs.

### Environment
The packages installed on the compute before your script runs (Python, scikit-learn, MLflow...). Azure provides ready-made **curated** environments. The notebooks pick a current one automatically.

### MLflow
An open-source tracking library. The training script logs the **regularization rate** (parameter), **Accuracy** and **AUC** (metrics), and the **ROC curve** (artifact) to the job.

### Hyperparameter tuning (sweep job)
A *hyperparameter* is a setting you choose before training, such as the regularization rate. A **sweep job** trains one model per value in a **search space**, compares them on a **primary metric** (here, `Accuracy`), and reports the best.

### Distributed and parallel training
There are two ways to use several machines:
- **Parallel trials (this lab):** each cluster node trains a *different* model at the same time. With 2 nodes and 4 trials, the sweep finishes in about half the time.
- **Distributed training of one model:** a single large model (usually deep learning with PyTorch or TensorFlow) is split across several nodes or GPUs. Azure ML supports it with the `distribution` and `instance_count` settings of a command job. It isn't needed for this small dataset, but the cluster you create here is the same kind of resource it would use.

## What was fixed compared with the original lab

So the lab runs first time, this version:
- uses a **setup script that doesn't produce errors to ignore**, registers the needed Azure services, and makes **every student's names unique** (a shared number makes compute instance creation fail when many people use the same region);
- picks a **current training environment automatically** (the old one is being retired);
- logs metrics only when running as a job, so the **script runs in any terminal**;
- uses the correct metric name for the sweep (`Accuracy`), so the **sweep job doesn't fail**;
- turns on **auto-shutdown** on the compute instance to protect your budget.

[⬅ Back to README](../README.md) | [Next: Prerequisites and cost ➡](01-prerequisites-and-cost.md)
