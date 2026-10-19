# Step 10 – Troubleshooting

[⬅ Back to README](../README.md)

Common errors in this lab, in the order you're likely to meet them.

| # | Where | Error |
|---|---|---|
| [T1](#t1-setupsh-subscription-is-not-registered-or-authorizationfailed) | Step 2 | Subscription not registered / AuthorizationFailed |
| [T2](#t2-setupsh-compute-instance-name-is-already-in-use--not-available) | Step 2 | Compute instance name already in use |
| [T3](#t3-cloud-shell-closed-or-timed-out-while-setupsh-was-running) | Step 2 | Cloud Shell closed during setup |
| [T4](#t4-quota-error-when-creating-compute-or-running-a-job) | Steps 2, 6, 7 | Quota error |
| [T5](#t5-workspace-creation-keeps-failing-create-everything-in-the-portal-instead) | Step 2 | Workspace creation keeps failing (manual fallback) |
| [T6](#t6-mlops-lab-folder-not-visible-in-the-files-pane) | Step 3 | Cloned folder not visible |
| [T7](#t7-importerror-libstdc-or-glibcxx-when-running-the-script) | Step 4 | ImportError libstdc++ / GLIBCXX |
| [T8](#t8-filenotfounderror-or-path-not-found-when-running-a-script) | Steps 4, 5 | File / path not found |
| [T9](#t9-notebook-kernel-or-authentication-problems) | Steps 4, 6, 7 | Kernel or authentication problems |
| [T10](#t10-the-command-job-or-sweep-job-failed) | Steps 6, 7 | Command or sweep job failed |
| [T11](#t11-job-stuck-in-queued-or-preparing) | Steps 6, 7 | Job stuck in Queued / Preparing |
| [T12](#t12-git-clone-asks-for-a-username-and-password) | Steps 2, 3 | git clone asks for a username and password |

---

### T1. setup.sh: "subscription is not registered" or "AuthorizationFailed"

- **`MissingSubscriptionRegistration`:** the script registers providers automatically. Wait 2 minutes, then run the **same** `bash setup.sh <suffix>` command again.
- **`AuthorizationFailed`:** you need **Contributor** or **Owner** on the subscription ([step 1.1](01-prerequisites-and-cost.md#11-check-your-role)). Ask your administrator, then reopen Cloud Shell and run the script again.
- **Wrong subscription:** run `az account list -o table`, then `az account set --subscription "<name or id>"`, then run the script again.

### T2. setup.sh: compute instance name "is already in use" / "not available"

**Cause:** compute instance names must be unique within the Azure **region**, and someone (often a classmate) already used your suffix.

**Fix:** delete the half-created resource group and start again with a different suffix:

```bash
cd ~/mlops-lab/infra
bash cleanup.sh
rm -f lab.env
bash setup.sh <a-new-unique-suffix>
```

### T3. Cloud Shell closed or timed out while setup.sh was running

Cloud Shell disconnects after about 20 minutes without activity, and with *No storage account required* your files are lost.

**Fix:** reopen Cloud Shell, clone again, and re-run with the **same** suffix. Existing resources are skipped:

```bash
git clone https://github.com/SHADRACK-NAKOBA/Azure-Model-training-Optimization.git ~/mlops-lab 2>/dev/null; cd ~/mlops-lab/infra
bash setup.sh <your-same-suffix>
```

### T4. Quota error when creating compute or running a job

**Messages:** `QuotaExceeded`, `Insufficient quota`, `Operation could not be completed as it results in exceeding approved ... quota`.

**Cause:** not enough *Standard DSv2 Family* vCPUs in your region (common on Free Trial). The lab needs up to 6.

**Fixes (pick one):**
- **Use another VM size** that has quota (keeps your current region):
  ```bash
  cd ~/mlops-lab/infra
  AZ_VM_SIZE=Standard_D2s_v3 bash setup.sh <your-suffix>
  ```
  If the compute instance already exists but the cluster failed, this just creates the cluster with the new size.
- **Use another region:** `bash cleanup.sh`, `rm -f lab.env`, then `bash setup.sh <new-suffix> westeurope` (or *northeurope*, *westus2*, *eastus2*).
- **Request more quota:** portal → **Quotas** → **Machine learning** → your region → *Standard DSv2 Family Cluster Dedicated vCPUs* → **Request quota increase** (ask for 8).

### T5. Workspace creation keeps failing: create everything in the portal instead

1. Portal → **+ Create a resource** → search **Azure Machine Learning** → **Create** → **New workspace**.
2. **Resource group:** *Create new* `rg-ai300-labs`. **Name:** `mlw-ai300-labs`. **Region:** closest to you. Leave storage, key vault and Application Insights as new defaults, and **Container registry: None**.
3. **Review + create** → **Create** → wait ~5 minutes → **Go to resource** → **Launch studio**.
4. Studio → **Compute** → **Compute instances** → **+ New** → give it a unique name (for example `ci-<yourinitials><date>`) → size **Standard_DS11_v2** → **Review + Create** → **Create**.
5. **Compute clusters** tab → **+ New** → same region, size **Standard_DS11_v2** → **Next** → name **`aml-cluster`** (exactly), min nodes **0**, max nodes **2** → **Create**.
6. Continue with [step 3](03-clone-lab-materials.md). The notebooks upload the data themselves, so you don't need to create data assets.

### T6. "mlops-lab" folder not visible in the Files pane

Click the **↻ Refresh** icon in the Files pane. If it's still missing, the clone ran in a different folder. In the compute instance terminal run:

```bash
cd ~/cloudfiles/code/Users/*/ && git clone https://github.com/SHADRACK-NAKOBA/Azure-Model-training-Optimization.git mlops-lab
```

### T7. ImportError: libstdc++ or GLIBCXX when running the script

Run these in the compute instance terminal, then run the script again:

```bash
sudo apt-get update
sudo apt-get install -y libstdc++6
```

If the error mentions a specific `GLIBCXX_3.4.xx` version that is still missing:

```bash
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install -y --only-upgrade libstdc++6
```

### T8. FileNotFoundError or "path not found" when running a script

The paths in the lab are **relative**, so they only work from the right folder:

```bash
# for experimentation/train-classification-model.py
cd ~/cloudfiles/code/Users/*/mlops-lab/experimentation
python train-classification-model.py

# for src/train-model-parameters.py
cd ~/cloudfiles/code/Users/*/mlops-lab/src
python train-model-parameters.py --training_data ../data/diabetes-data/diabetes.csv
```

`ERROR: no training data given` in step 5.2 is **expected**. It's part of the lab.

### T9. Notebook kernel or authentication problems

| Symptom | Fix |
|---|---|
| *No kernel* / kernel keeps disconnecting | Check the compute instance is **Running** (Compute page). Then click the kernel name → choose **Python 3.10 - SDK v2**. |
| `ModuleNotFoundError: No module named 'azure.ai.ml'` | Run the `%pip install ...` cell, click **⟳ Restart kernel**, then run the cells again from the top. |
| `ModuleNotFoundError: No module named 'lab_helpers'` | The notebook must stay in the **experimentation** folder next to `lab_helpers.py`. Don't move or copy it elsewhere. |
| An **Authenticate** banner, or `DefaultAzureCredential failed` | Click **Authenticate** and sign in, then run the cell again. If a browser sign-in link is printed, open it and sign in. |
| `Could not find the workspace configuration` | You're running the notebook on your own computer. Run it in the studio's **Notebooks** page on your compute instance. |

### T10. The command job or sweep job failed

Open the job → **Outputs + logs** → **user_logs/std_log.txt** (for a sweep, open the failed **trial** first).

| Message contains | Fix |
|---|---|
| `Compute target aml-cluster not found` | The cluster is missing or has a different name. Check **Compute → Compute clusters**. It must be named exactly **aml-cluster**. Create it as in [T5](#t5-workspace-creation-keeps-failing-create-everything-in-the-portal-instead) step 5. |
| `Environment ... not found` / `deprecated` | Re-run the `get_sklearn_environment` cell. It picks a current environment, or builds the custom fallback (the first build adds ~10 minutes). |
| `QuotaExceeded` | See [T4](#t4-quota-error-when-creating-compute-or-running-a-job). |
| `NameError` / `ModuleNotFoundError: pandas` in std_log | You edited the script (for example the optional "remove import" test). Restore the line, save, resubmit. |
| Sweep: `primary metric ... not found` | The metric name must be exactly **`Accuracy`** (capital A), the same as `log_metric("Accuracy", ...)` in the script. Don't rename it in only one place. |
| `Image build failed` | Only for the custom fallback environment. Resubmit once (registry creation can be slow on first use). If it fails again, check **Microsoft.ContainerRegistry** is *Registered* on your subscription. |

### T11. Job stuck in "Queued" or "Preparing"

- **Queued** for up to ~5 minutes is normal while the cluster starts a node from 0.
- **Preparing** for up to ~10 minutes is normal the first time an environment is used (longer with the custom fallback environment).
- Longer than 20 minutes: open the job's **Overview** and look for a quota or capacity warning ([T4](#t4-quota-error-when-creating-compute-or-running-a-job)). Click **Cancel**, then resubmit.

### T12. git clone asks for a username and password

The repo must be **public**. On GitHub, the repo owner goes to **Settings → General → Danger Zone → Change visibility → Make public**. Also check the URL is typed exactly:
`https://github.com/SHADRACK-NAKOBA/Azure-Model-training-Optimization.git`

---

Still stuck? Post a screenshot of the **full error message** (hide your subscription ID) and the step number in the Prince community lab issues thread.

[⬅ Back to README](../README.md)
