# Step 3 – Clone the lab materials onto your compute instance

[⬅ Previous: Provision the workspace](02-provision-workspace.md) | [Next: Convert a notebook to a script ➡](04-convert-notebook-to-script.md)

With the workspace and compute ready, open the studio and copy this repo onto your compute instance, where you'll run the notebooks and the terminal.

## 3.1 Open the studio

1. In the Azure portal search bar, type **`mlw-ai300`** and click your workspace **mlw-ai300-l<suffix>**.
   (Or: **Resource groups** → **rg-ai300-l<suffix>** → the *Azure Machine Learning workspace*.)
2. On the **Overview** page, click **Launch studio**. The studio opens in a new tab.
   > Nothing happened? Allow pop-ups for portal.azure.com (blocked pop-up icon at the right of the address bar), or go to https://ml.azure.com and pick your workspace.
3. Close any pop-ups in the studio.

## 3.2 Check your compute

1. In the left menu, under **Manage**, click **Compute**.
2. **Compute instances** tab: **ci<suffix>** should show **State: Running**.
   - If it says *Stopped*, tick it and click **Start**. Wait 2–3 minutes until it shows *Running*.
3. **Compute clusters** tab: **aml-cluster** should show **Succeeded**, with **0** nodes running (it only starts nodes when a job runs).

## 3.3 Open the terminal and clone the repo

1. Go back to the **Compute instances** tab. In the **Applications** column of your instance, click **Terminal**.
   (Can't see it? Click the instance name, then the **Terminal** link under *Applications*.)
2. A terminal opens in your user folder. Paste these commands and press **Enter**:

   ```bash
   rm -rf mlops-lab
   git clone https://github.com/SHADRACK-NAKOBA/Azure-Model-training-Optimization.git mlops-lab
   ```

3. Check it worked:

   ```bash
   ls mlops-lab
   ```

   You should see `README.md  data  docs  experimentation  infra  src`.

> **About installing the SDK:** the original lab ran `pip uninstall azure-ai-ml` / `pip install azure-ai-ml` here. That isn't needed any more. In the terminal, `pip` installs into a *different* Python environment than the notebook kernel, so it didn't help anyway. The notebooks now install or update the SDK in the correct place in their first cell.

## 3.4 See the files in the studio

1. In the left menu, under **Authoring**, click **Notebooks**.
2. In the **Files** pane, click the **↻ (Refresh)** icon.
3. Expand **Users** → *your-user-name* → **mlops-lab**. You'll see the `experimentation`, `src` and `data` folders.

## Check before you continue

- [ ] **ci<suffix>** is *Running* and **aml-cluster** is *Succeeded*.
- [ ] You can see **Users/*your-user-name*/mlops-lab** in the Files pane.

[⬅ Previous: Provision the workspace](02-provision-workspace.md) | [Next: Convert a notebook to a script ➡](04-convert-notebook-to-script.md)
