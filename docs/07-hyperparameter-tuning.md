# Step 7 – Optimize with hyperparameter tuning

[⬅ Previous: Run the script as a command job](06-run-command-job.md) | [Next: Share your learnings ➡](08-share-your-learnings.md)

The regularization rate is a **hyperparameter**: a setting chosen before training that affects how well the model fits. Instead of trying values one at a time by hand, you'll run a **sweep job**. It trains one model per value, compares them on `Accuracy`, and reports the best.

To save time, the sweep runs **two trials at the same time**, one on each node of `aml-cluster`. This is how you use several compute resources to cut total training time.

## 7.1 Submit the sweep job

1. Open **mlops-lab/experimentation/hyperparameter-tuning.ipynb**.
2. Check **Compute** = **ci<suffix>** and **Kernel** = **Python 3.10 - SDK v2**.
3. Click **▷▷ Run all**, or run the cells one at a time. Read the explanation above each cell:
   - **Search space:** `reg_rate` = `0.01`, `0.1`, `1`, `10`, which is 4 models
   - **Sampling:** `grid` (try every value)
   - **Primary metric:** `Accuracy` (must match the name the script logs with MLflow), goal **Maximize**
   - **Limits:** 4 trials in total, **2 at the same time**, 1-hour timeout
4. Click the **Monitor your job at** link.

⏱️ The sweep takes **10–20 minutes**. The cluster scales from 0 to 2 nodes, runs two trials, then the next two.

## 7.2 Review the results

When **diabetes-sweep-reg-rate** shows **Completed**:

1. **Overview** tab: the **best trial** and its Accuracy.
2. **Trials** tab: all four trials. Tick all four to compare them in the chart and the table:
   - which `reg_rate` gave the highest **Accuracy**,
   - how the trial start times overlap (two ran in parallel).
3. Click a trial to see its **Params**, **Metrics** and **ROC curve**, just like the command job.
4. *(Optional)* Run the last cell in the notebook to print the sweep's status and best score.

> **What to expect:** all four accuracies are close (around **0.77**). That's a real finding, not a mistake. For this model and data, regularization makes little difference, so a better result would need a different algorithm or more features. Finding that out *automatically* and in *parallel*, instead of by trial and error, is the point of tuning.

## Check before you continue

- [ ] The sweep job is **Completed** with 4 trials.
- [ ] You know which regularization rate gave the best Accuracy.
- [ ] 📸 Screenshot the **Trials** tab for step 8.

[⬅ Previous: Run the script as a command job](06-run-command-job.md) | [Next: Share your learnings ➡](08-share-your-learnings.md)
