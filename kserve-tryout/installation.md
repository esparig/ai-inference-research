# Check Kubernetes and kubectl version
k version

# check cert-manager version
k get deployment cert-manager -n cert-manager -o=jsonpath="{.spec.template.spec.containers[0].image}"

# Network Controller -> Ingress controllers
k get deployment -n ingress-nginx ingress-nginx-controller -o=jsonpath="{.spec.template.spec.containers[0].image}"

# Install KServe (from oscar-cham machine)
sudo helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd --version v0.15.0

# Install KServe Resources & Set the kserve.controller.deploymentMode to Standard and configure the Ingress class
sudo kubectl create namespace kserve

sudo helm install kserve oci://ghcr.io/kserve/charts/kserve --version v0.15.0  --namespace kserve --create-namespace --set kserve.controller.deploymentMode=RawDeployment   --set kserve.controller.gateway.ingressGateway.className="nginx"

# Patch inference config
k apply -f /home/esparig/projects/ai-inference-research/kserve-tryout/inference-config-patch-job.yaml

# Deploy a sample inference service https://kserve.github.io/archive/0.15/get_started/first_isvc/

k create namespace kserve-test

k apply -n kserve-test -f /home/esparig/projects/ai-inference-research/kserve-tryout/sklearn-iris.yaml