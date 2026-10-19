# Step 9 – Delete resources

[⬅ Previous: Share your learnings](08-share-your-learnings.md) | [Next: Troubleshooting ➡](10-troubleshooting.md)

If you don't plan to do more exercises, delete the resources now so you don't keep paying for them. Deleting the **resource group** deletes everything in it: workspace, compute instance, cluster, storage, key vault and monitoring.

> ⚠️ Save your screenshots first. Deleting can't be undone.

## Option A – Azure portal (click by click)

1. Close the Azure Machine Learning studio tab.
2. Go to https://portal.azure.com → **Resource groups** (on the Home page, or type it in the search bar).
3. Click your **rg-ai300-l<suffix>** resource group.
4. Click **Delete resource group** at the top of the Overview page.
5. Type the resource group name in the confirmation box (for example `rg-ai300-lsn1019`).
6. Click **Delete**, then **Delete** again if asked.
7. Click the **bell** icon (top right) to follow progress. It takes **5–10 minutes**.
8. Refresh **Resource groups**. Your **rg-ai300-l…** group should be gone.

## Option B – Cloud Shell

```bash
cd ~/mlops-lab/infra
bash cleanup.sh
```

If Cloud Shell was reset and the script can't find your names, give the resource group name yourself:

```bash
cd ~/mlops-lab/infra 2>/dev/null || git clone https://github.com/SHADRACK-NAKOBA/Azure-Model-training-Optimization.git ~/mlops-lab && cd ~/mlops-lab/infra
bash cleanup.sh rg-ai300-lsn1019
```

## Repeating the lab later?

Azure keeps a deleted workspace in a *soft-deleted* state for 14 days. Use a **new suffix** when you run `setup.sh` again and you won't hit a name conflict.

[⬅ Previous: Share your learnings](08-share-your-learnings.md) | [Next: Troubleshooting ➡](10-troubleshooting.md)
