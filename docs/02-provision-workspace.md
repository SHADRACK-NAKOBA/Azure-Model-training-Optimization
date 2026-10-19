# Step 2 – Provision the workspace and compute

[⬅ Previous: Prerequisites and cost](01-prerequisites-and-cost.md) | [Next: Clone the lab materials ➡](03-clone-lab-materials.md)

You can work with a workspace through the studio, the Python SDK and the Azure CLI. Here you use the **Azure CLI** to create the workspace and compute (one script does it all), and later the **Python SDK** to run jobs.

## 2.1 Open Cloud Shell

1. Go to https://portal.azure.com and sign in.
2. Click the **`>_`** (Cloud Shell) icon in the top bar, to the right of the search box. A terminal pane opens at the bottom of the page.
3. If asked, choose **Bash**. If it opens in *PowerShell*, click **Switch to Bash** in the Cloud Shell toolbar.
4. If you see **Getting started**:
   - choose **No storage account required**,
   - check the **Subscription** is the one you want,
   - click **Apply**.

> **Pasting into Cloud Shell:** right-click → **Paste**, or press **Ctrl + Shift + V** (Windows) / **Cmd + V** (Mac). If Ctrl + V doesn't work, try **Shift + Insert**.

## 2.2 Clone this repo into Cloud Shell

Paste these commands and press **Enter**:

```bash
rm -rf mlops-lab
git clone https://github.com/SHADRACK-NAKOBA/Azure-Model-training-Optimization.git mlops-lab
```

You should see `Cloning into 'mlops-lab'...` followed by `done`.

## 2.3 Choose your suffix

The script adds a **suffix** to every name to keep them unique. **Each student must use a different suffix.** Compute instance names must be unique in the whole Azure region, so two students using the same suffix will make the second one's setup fail.

- Choose **4–18 lowercase letters and numbers**, for example your initials plus today's date: `sn1019`.
- Or leave it out, and the script creates a random one for you.

## 2.4 Run the setup script

Replace `sn1019` with **your** suffix, then paste:

```bash
cd ~/mlops-lab/infra
bash setup.sh sn1019
```

To use a region other than East US (for example because that's where you have quota), add it at the end:

```bash
bash setup.sh sn1019 westeurope
```

The script will:

1. show the names it is going to create,
2. register the Azure services the lab needs (first time only),
3. install the Azure ML CLI extension,
4. create the resource group **`rg-ai300-l<suffix>`** and workspace **`mlw-ai300-l<suffix>`**,
5. create the compute instance **`ci<suffix>`** (with 60-minute auto-shutdown) and the compute cluster **`aml-cluster`**,
6. create the data assets **diabetes-training** and **diabetes-data**.

⏱️ It takes **10–15 minutes**. Leave Cloud Shell open. If it closes, see [Troubleshooting T3](10-troubleshooting.md#t3-cloud-shell-closed-or-timed-out-while-setupsh-was-running).

When it finishes you'll see:

```
============================================================
 DONE. Write these names down:
   Resource group:    rg-ai300-lsn1019
   Workspace:         mlw-ai300-lsn1019
   Compute instance:  cisn1019
   Compute cluster:   aml-cluster
```

📝 **Write down your names.** They're also saved in `~/mlops-lab/infra/lab.env`.

> ❌ If the script stops with an error, read the last red lines and look them up in [Troubleshooting](10-troubleshooting.md). You can safely run the **same command again**: the script skips anything that already exists.

## Check before you continue

- [ ] The script ended with **DONE**.
- [ ] You've written down your resource group, workspace and compute instance names.

[⬅ Previous: Prerequisites and cost](01-prerequisites-and-cost.md) | [Next: Clone the lab materials ➡](03-clone-lab-materials.md)
