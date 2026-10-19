# Step 1 – Prerequisites and cost

[⬅ Previous: Overview](00-overview-and-concepts.md) | [Next: Provision the workspace ➡](02-provision-workspace.md)

## Prerequisites

- An Azure subscription (Free Trial, Pay-As-You-Go or paid). To create one: https://azure.microsoft.com/free
- The **Owner** or **Contributor** role on that subscription.
- **A billing alert** (1.2 below), so you're warned before costs grow.
- **Chrome** or **Edge**.

## 1.1 Check your role

1. Sign in to https://portal.azure.com.
2. In the top search bar, type **`Subscriptions`** and click **Subscriptions**.
3. Click your subscription → **Access control (IAM)** in the left menu → **View my access**.
4. Check that you have **Owner** or **Contributor**. If you only have *Reader*, ask your administrator for Contributor before continuing.

## 1.2 Create a billing alert (budget)

1. In the top search bar, type **`Budgets`** and click **Budgets** (under *Cost Management*).
2. If asked for a scope, choose your **subscription**.
3. Click **+ Add**.
4. **Create budget** tab:
   - **Name:** `lab-budget`
   - **Reset period:** *Monthly*
   - **Amount:** `10` (or whatever limit you're comfortable with)
   - Click **Next**.
5. **Set alerts** tab:
   - Under **Alert conditions**: Type **Actual**, **% of budget** `80`.
   - **Alert recipients (email):** your email address.
   - Click **Create**.

> A budget **warns** you; it doesn't stop resources. Deleting the resources in [step 9](09-cleanup.md) is what stops the charges.

## 1.3 Check VM quota (prevents "insufficient quota" errors)

The lab uses **Standard_DS11_v2** VMs (2 vCPUs each, *Standard DSv2 Family*): 1 compute instance plus up to 2 cluster nodes, so **6 vCPUs** at most.

1. In the top search bar, type **`Quotas`** and click **Quotas** → **Machine learning**.
2. Filter on your **subscription** and region **East US** (the default region the setup script uses).
3. Search for **`DSv2`** and look at **Standard DSv2 Family Cluster Dedicated vCPUs**.
4. You need **at least 6 free** (limit minus usage).

- **Enough?** Continue.
- **Not enough** (common on Free Trial)? Pick a region with quota and pass it to the setup script in step 2, use a different VM size (`AZ_VM_SIZE=Standard_D2s_v3`, see [Troubleshooting T4](10-troubleshooting.md#t4-quota-error-when-creating-compute-or-running-a-job)), or click **Request quota increase**.

---

## Cost to perform the lab

**Typical total: about US $0.50–$2.00** for 1–2 hours, as long as you delete everything at the end.

| Resource | When you pay | Rough cost |
|---|---|---|
| Compute instance (Standard_DS11_v2) | **Every hour it's running** | Around $0.20–0.30 per hour |
| Compute cluster nodes (Standard_DS11_v2) | Only while jobs run, per node | Around $0.20–0.30 per node per hour |
| Storage, key vault, monitoring | Tiny amounts | Cents |

Exact prices depend on region and currency: https://azure.microsoft.com/en-us/pricing/details/machine-learning/

> 💡 **Biggest cost risk:** a compute instance left running. It auto-stops after 60 idle minutes in this lab, but stop it yourself when you take a break (**Compute → Compute instances → tick it → Stop**), and delete everything in [step 9](09-cleanup.md).

[⬅ Previous: Overview](00-overview-and-concepts.md) | [Next: Provision the workspace ➡](02-provision-workspace.md)
