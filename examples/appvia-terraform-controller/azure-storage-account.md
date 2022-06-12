## Install/Upgrade Terraform Controller
```bash
helm install -n terraform-system terraform-controller appvia/terraform-controller --create-namespace
```

## Create secret based of Service Principal with Contributor role
```bash
kubectl -n terraform-system create secret generic azure \
  --from-literal=ARM_CLIENT_ID="${ARM_CLIENT_ID}" \
  --from-literal=ARM_CLIENT_SECRET="${ARM_CLIENT_SECRET}" \
  --from-literal=ARM_SUBSCRIPTION_ID="${ARM_SUBSCRIPTION_ID}" \
  --from-literal=ARM_TENANT_ID="${ARM_TENANT_ID}"
```

## Create provider
```bash
kubectl apply -f azure.yaml
```

## Run tf2helm to convert Azure Storage Account TF module to Helm Chart
```bash
tf2helm --tf-module-url "https://github.com/Azure-Terraform/terraform-azurerm-storage-account.git?ref=v0.14.0" \
  --name azure-blob-storage \
  --app-version 0.1.0 \
  --output-dir .
```
## Render Helm template to validate configuration
```bash
helm template -n apps azure-blob-storage ./azure-blob-storage --dry-run --debug \
  --set optional.shared_access_key_enabled=true \
  --set optional.default_network_rule="Allow" \
  --set optional.name="terranetesdemostore123" \
  --set required.location="uksouth" \
  --set required.replication_type="LRS" \
  --set required.resource_group_name="terranetes-demo" \
  --set required.tags.managed_by="terraform-controller" \
  --set required.enable_auto_approval=true \
  --set required.provider_ref="azure"
```

## Install / Upgrade Azure storage account
```bash
helm upgrade -i -n apps azure-blob-storage ./azure-blob-storage  \
  --set optional.shared_access_key_enabled=true \
  --set optional.default_network_rule="Allow" \
  --set optional.name="terranetesdemostore123" \
  --set required.location="uksouth" \
  --set required.replication_type="LRS" \
  --set required.resource_group_name="terranetes-demo" \
  --set required.tags.managed_by="terraform-controller" \
  --set required.enable_auto_approval=true \
  --set required.provider_ref="azure"
```

## Clean up resources
```bash
helm uninstall -n apps azure-blob-storage
kubectl -n apps delete po --all
```
