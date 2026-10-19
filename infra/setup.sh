#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Prince Hands-on Lab - Optimize model training in Azure Machine Learning
#
# Creates everything the lab needs:
#   - resource group      rg-ai300-l<suffix>
#   - ML workspace        mlw-ai300-l<suffix>
#   - compute instance    ci<suffix>      (Standard_DS11_v2, auto-stops after 60 idle minutes)
#   - compute cluster     aml-cluster     (Standard_DS11_v2, 0-2 nodes, scales to 0 when idle)
#   - data assets         diabetes-training (MLTable) and diabetes-data (CSV file)
#
# Run in Azure Cloud Shell (Bash), from this folder:
#     bash setup.sh                      # random suffix, region eastus
#     bash setup.sh 1234abcd             # your own suffix
#     bash setup.sh 1234abcd westeurope  # your own suffix and region
#
# Safe to re-run with the same suffix: anything that already exists is skipped.
# -----------------------------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="${SCRIPT_DIR}/lab.env"

# --- 1. Names ----------------------------------------------------------------
# The suffix makes your names unique. Compute instance names must be unique in
# the whole Azure region, so everyone in a class needs a DIFFERENT suffix.
if [[ -n "${1:-}" ]]; then
  SUFFIX="$(echo "$1" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9')"
elif [[ -f "$ENV_FILE" ]]; then
  # re-use the suffix from a previous run of this script
  SUFFIX="$(grep '^SUFFIX=' "$ENV_FILE" | cut -d= -f2)"
else
  SUFFIX="$(tr -dc 'a-z0-9' < /dev/urandom | head -c 8 || true)"
fi
if [[ ${#SUFFIX} -lt 4 || ${#SUFFIX} -gt 18 ]]; then
  echo "ERROR: the suffix must be 4-18 letters/numbers (you gave '${1:-}')." >&2
  exit 1
fi

LOCATION="${2:-${AZ_LOCATION:-eastus}}"
RESOURCE_GROUP="rg-ai300-l${SUFFIX}"
WORKSPACE_NAME="mlw-ai300-l${SUFFIX}"
COMPUTE_INSTANCE="ci${SUFFIX}"
COMPUTE_CLUSTER="aml-cluster"
VM_SIZE="${AZ_VM_SIZE:-Standard_DS11_v2}"

echo "============================================================"
echo " Subscription:      $(az account show --query name -o tsv)"
echo " Suffix:            ${SUFFIX}"
echo " Region:            ${LOCATION}"
echo " Resource group:    ${RESOURCE_GROUP}"
echo " Workspace:         ${WORKSPACE_NAME}"
echo " Compute instance:  ${COMPUTE_INSTANCE}"
echo " Compute cluster:   ${COMPUTE_CLUSTER}"
echo " VM size:           ${VM_SIZE}"
echo "============================================================"

# Save the names so cleanup.sh (and you) can find them later.
cat > "$ENV_FILE" <<EOF
SUFFIX=${SUFFIX}
LOCATION=${LOCATION}
RESOURCE_GROUP=${RESOURCE_GROUP}
WORKSPACE_NAME=${WORKSPACE_NAME}
COMPUTE_INSTANCE=${COMPUTE_INSTANCE}
COMPUTE_CLUSTER=${COMPUTE_CLUSTER}
EOF
echo "Names saved to infra/lab.env"

# --- 2. Resource providers (prevents 'subscription is not registered') --------
for p in Microsoft.MachineLearningServices Microsoft.Storage Microsoft.KeyVault \
         Microsoft.Insights Microsoft.OperationalInsights Microsoft.ContainerRegistry; do
  state=$(az provider show --namespace "$p" --query registrationState -o tsv 2>/dev/null || echo NotRegistered)
  if [[ "$state" != "Registered" ]]; then
    echo "Registering resource provider $p (can take a few minutes)..."
    az provider register --namespace "$p" --wait
  fi
done
echo "Resource providers: OK"

# --- 3. Azure ML CLI extension (removes the conflicting old v1 extension) ----
if az extension show -n azure-cli-ml >/dev/null 2>&1; then
  az extension remove -n azure-cli-ml
fi
az extension add -n ml --upgrade -y --only-show-errors
echo "Azure ML CLI extension: OK"

# --- 4. Resource group and workspace -----------------------------------------
echo "Creating resource group..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" -o none

if az ml workspace show -n "$WORKSPACE_NAME" -g "$RESOURCE_GROUP" -o none 2>/dev/null; then
  echo "Workspace already exists - skipping"
else
  echo "Creating workspace (about 3-5 minutes)..."
  az ml workspace create -n "$WORKSPACE_NAME" -g "$RESOURCE_GROUP" -l "$LOCATION" -o none
fi
WS=(--resource-group "$RESOURCE_GROUP" --workspace-name "$WORKSPACE_NAME")

# --- 5. Compute instance (for notebooks and the terminal) ---------------------
TMP_YML="$(mktemp --suffix .yml)"
if az ml compute show -n "$COMPUTE_INSTANCE" "${WS[@]}" -o none 2>/dev/null; then
  echo "Compute instance already exists - skipping"
else
  echo "Creating compute instance ${COMPUTE_INSTANCE} (about 5 minutes)..."
  cat > "$TMP_YML" <<EOF
\$schema: https://azuremlschemas.azureedge.net/latest/computeInstance.schema.json
name: ${COMPUTE_INSTANCE}
type: computeinstance
size: ${VM_SIZE}
idle_time_before_shutdown_minutes: 60
EOF
  az ml compute create --file "$TMP_YML" "${WS[@]}" -o none
fi

# --- 6. Compute cluster (runs the command and sweep jobs) ---------------------
if az ml compute show -n "$COMPUTE_CLUSTER" "${WS[@]}" -o none 2>/dev/null; then
  echo "Compute cluster already exists - skipping"
else
  echo "Creating compute cluster ${COMPUTE_CLUSTER}..."
  cat > "$TMP_YML" <<EOF
\$schema: https://azuremlschemas.azureedge.net/latest/amlCompute.schema.json
name: ${COMPUTE_CLUSTER}
type: amlcompute
size: ${VM_SIZE}
min_instances: 0
max_instances: 2
idle_time_before_scale_down: 120
EOF
  az ml compute create --file "$TMP_YML" "${WS[@]}" -o none
fi
rm -f "$TMP_YML"

# --- 7. Data assets -------------------------------------------------------------
if az ml data show -n diabetes-training --version 1 "${WS[@]}" -o none 2>/dev/null; then
  echo "Data asset diabetes-training already exists - skipping"
else
  echo "Creating data asset diabetes-training (MLTable)..."
  az ml data create --type mltable --name diabetes-training --version 1 \
    --path "${REPO_DIR}/data/diabetes-data" "${WS[@]}" -o none
fi
if az ml data show -n diabetes-data --version 1 "${WS[@]}" -o none 2>/dev/null; then
  echo "Data asset diabetes-data already exists - skipping"
else
  echo "Creating data asset diabetes-data (CSV file)..."
  az ml data create --type uri_file --name diabetes-data --version 1 \
    --path "${REPO_DIR}/data/diabetes-data/diabetes.csv" "${WS[@]}" -o none
fi

echo
echo "============================================================"
echo " DONE. Write these names down:"
echo "   Resource group:    ${RESOURCE_GROUP}"
echo "   Workspace:         ${WORKSPACE_NAME}"
echo "   Compute instance:  ${COMPUTE_INSTANCE}"
echo "   Compute cluster:   ${COMPUTE_CLUSTER}"
echo " Next: open https://ml.azure.com and select workspace ${WORKSPACE_NAME}"
echo "============================================================"
