# Step 6 – Run the script as a command job

[⬅ Previous: Test a script in the terminal](05-test-script-in-terminal.md) | [Next: Optimize with hyperparameter tuning ➡](07-hyperparameter-tuning.md)

Once you know the script works, run it as a **command job**. Azure Machine Learning then tracks all of its inputs, outputs, logs and metrics, and runs it on the compute cluster instead of your compute instance.

## 6.1 Submit the job

1. In **Files**, open **mlops-lab/experimentation/run-script-as-command-job.ipynb**.
2. Check **Compute** = your **ci<suffix>** instance and **Kernel** = **Python 3.10 - SDK v2** (as in [step 4.1](04-convert-notebook-to-script.md#41-open-and-run-the-notebook)).
3. Run the cells **one at a time** with **Shift + Enter** (or click **▷▷ Run all**):

   | Cell | What you should see |
   |---|---|
   | `%pip install ...` | Installs or updates the SDK. If it says *restart the kernel*, click the **⟳ Restart kernel** icon, then continue from the next cell. |
   | `get_ml_client()` | `Connected to workspace: mlw-ai300-l<suffix>`. If an **Authenticate** banner appears, click it, sign in, and run the cell again. |
   | `get_sklearn_environment(...)` | `Using curated environment: ...` (or, rarely, `Using custom environment: ...`) |
   | `command(...)` + submit | `Job name: ...` and `Monitor your job at https://ml.azure.com/...` |
   | `ml_client.jobs.stream(...)` *(optional)* | The job's live log, until it says `Execution Summary` with **Status: Completed** |

4. Click the **Monitor your job at** link (or go to **Jobs** in the left menu).

⏱️ The first job takes **5–10 minutes**. The cluster has to start a node and prepare the environment. Status goes *Queued* → *Preparing* → *Running* → **Completed**.

## 6.2 Explore the job

1. Left menu → **Jobs** → **All experiments** → **diabetes-training** → click **diabetes-train-script**.
2. **Overview** tab: status, duration, compute (*aml-cluster*), and under **Params**: `Regularization rate = 0.01`.
3. **Metrics** tab: **Accuracy** (~0.774) and **AUC** (~0.848), logged by MLflow.
4. **Images** tab: the **ROC-Curve** plot.
5. **Code** tab: a snapshot of the whole **src** folder, the `code` setting of the job. This is exactly the script that ran.
6. **Outputs + logs** tab: open **user_logs → std_log.txt**. It contains the same output you saw in the terminal in step 5. If a job fails because of the script, the error is here.

**Optional:** remove `import pandas as pd` from **src/train-model-parameters.py**, save, and run the submit cell again. Look at the failed job's **std_log.txt** to see how errors show up. Put the line back afterwards.

## Check before you continue

- [ ] **diabetes-train-script** has status **Completed**.
- [ ] You found the parameter, the two metrics, the ROC curve image and **std_log.txt**.
- [ ] 📸 Screenshot the job **Overview** and **Metrics** tabs for step 8.

[⬅ Previous: Test a script in the terminal](05-test-script-in-terminal.md) | [Next: Optimize with hyperparameter tuning ➡](07-hyperparameter-tuning.md)
