# Step 4 – Convert a notebook to a script

[⬅ Previous: Clone the lab materials](03-clone-lab-materials.md) | [Next: Test a script in the terminal ➡](05-test-script-in-terminal.md)

A notebook on a compute instance is ideal for experimenting: you run code and see the result immediately. To move from development to production, you'll want scripts. The first step is converting the notebook to a script in the studio.

## 4.1 Open and run the notebook

1. In **Notebooks** → **Files**, open **Users/*your-user-name*/mlops-lab/experimentation/train-classification-model.ipynb**.
2. If a banner asks you to **Authenticate**, click it and follow the sign-in steps.
3. **Compute** (top of the notebook): make sure your **ci<suffix>** instance is selected and shows a green dot (running).
4. **Kernel** (top right of the notebook): it should say **Python 3.10 - SDK v2**.
   - If it says something else or *No kernel*, click it and choose **Python 3.10 - SDK v2**.
   - If that exact name isn't listed, choose the newest **Python 3.10** kernel offered.
5. Click **▷▷ Run all** in the notebook toolbar.
6. Scroll through the output. You'll see the data preview, then `Accuracy: 0.774...` and `AUC: 0.848...`, and the last cell saves the ROC curve.

## 4.2 Export the notebook as a Python script

1. Click the **☰** (notebook menu) icon at the top left of the notebook toolbar.
2. Hover over / expand **Export as** and click **Python (.py)**.
3. Name the file **`train-classification-model`** and click **Export**.
4. The new file **experimentation/train-classification-model.py** opens automatically. Look through it: it's the same code as the notebook, just in one file.

## 4.3 Run the script

1. With **train-classification-model.py** open, click the **▷▷ (Save and run script in terminal)** icon at the top of the file.
2. A terminal opens and runs `python train-classification-model.py`. The output ends with:

   ```
   Reading data...
   Splitting data...
   Training model...
   Accuracy: 0.774
   AUC: 0.848...
   ROC curve saved to ROC-Curve.png
   ```

> ❌ **`FileNotFoundError: ../data/diabetes-data/diabetes.csv`**: the terminal isn't in the `experimentation` folder. Run:
> ```bash
> cd ~/cloudfiles/code/Users/*/mlops-lab/experimentation
> python train-classification-model.py
> ```
> ❌ **`ImportError` mentioning `libstdc++` or `GLIBCXX`**: see [Troubleshooting T7](10-troubleshooting.md#t7-importerror-libstdc-or-glibcxx-when-running-the-script).

## Check before you continue

- [ ] The notebook ran all cells without errors.
- [ ] **train-classification-model.py** exists and printed Accuracy and AUC in the terminal.

[⬅ Previous: Clone the lab materials](03-clone-lab-materials.md) | [Next: Test a script in the terminal ➡](05-test-script-in-terminal.md)
