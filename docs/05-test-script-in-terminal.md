# Step 5 – Test a script in the terminal

[⬅ Previous: Convert a notebook to a script](04-convert-notebook-to-script.md) | [Next: Run the script as a command job ➡](06-run-command-job.md)

A converted notebook is a start, but production scripts should be organised into **functions** (easier to unit test) and use **parameters** (so you can change the data or settings without editing code).

## 5.1 Explore the production script

1. In **Files**, open **mlops-lab/src/train-model-parameters.py**.
2. Find the **`main`** function. It calls four other functions, one per task:
   - **`get_data`**: read the data (one CSV file, or a folder of CSV files)
   - **`split_data`**: split it into training and test sets
   - **`train_model`**: train a logistic regression model
   - **`eval_model`**: calculate Accuracy and AUC and plot the ROC curve
3. Below `main`, look at how each function is defined and what it takes in and returns.
4. Scroll to **`parse_args()`** at the bottom. It defines two input parameters:
   - **`--training_data`**: a string, the path to the data. **It has no default.**
   - **`--reg_rate`**: a number, the regularization rate. Default **0.01**.

## 5.2 Run it without parameters (on purpose)

1. With **train-model-parameters.py** open, click **▷▷ (Save and run script in terminal)**.
2. You get an error right after **Reading data...**:

   ```
   ERROR: no training data given. Add --training_data <path to csv or folder>, e.g.
       python train-model-parameters.py --training_data ../data/diabetes-data/diabetes.csv
   ```

   ✅ This is expected. The script needs to be told where the data is.

## 5.3 Run it with parameters

In the terminal, paste:

```bash
cd ~/cloudfiles/code/Users/*/mlops-lab/src
python train-model-parameters.py --training_data ../data/diabetes-data/diabetes.csv
```

The output shows:

```
Reading data...
Read 10,000 rows
Splitting data...
Training model (regularization rate 0.01)...
Accuracy: 0.774
AUC: 0.848...
```

Now try a different regularization rate, without changing any code:

```bash
python train-model-parameters.py --training_data ../data/diabetes-data/diabetes.csv --reg_rate 1
```

> Testing in the terminal is the quickest way to check a script works. If there's a problem in the code, you see the error right away, before spending money on cloud compute.

**Optional:** to see what a code error looks like, delete the line `import pandas as pd` from the script, save it (**Ctrl + S**), and run the command again. Read the error, then put the line back and save.

## Check before you continue

- [ ] The script printed **Accuracy** and **AUC** when run with `--training_data`.
- [ ] If you did the optional test, `import pandas as pd` is back in the script.

[⬅ Previous: Convert a notebook to a script](04-convert-notebook-to-script.md) | [Next: Run the script as a command job ➡](06-run-command-job.md)
