# KServe Installation and Tryout Guide

1. **Check Kubernetes and kubectl version**
   ```bash
   k version
   ```

2. **Check cert-manager version**
   ```bash
   k get deployment cert-manager -n cert-manager -o=jsonpath="{.spec.template.spec.containers[0].image}"
   ```

3. **Network Controller -> Ingress controllers**
   ```bash
   k get deployment -n ingress-nginx ingress-nginx-controller -o=jsonpath="{.spec.template.spec.containers[0].image}"
   ```

4. **Install KServe**
   ```bash
   helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd --version v0.15.0 --kube-insecure-skip-tls-verify
   ```

5. **Install KServe Resources & Set the kserve.controller.deploymentMode to RawDeployment and configure the Ingress class**
   ```bash
   k create namespace kserve

   helm install kserve oci://ghcr.io/kserve/charts/kserve --version v0.15.0  --namespace kserve --create-namespace --set kserve.controller.deploymentMode=RawDeployment --set kserve.controller.gateway.ingressGateway.className="nginx" --kube-insecure-skip-tls-verify
   ```

6. **Patch inference config**
   ```bash
   k apply -f /home/esparig/projects/ai-inference-research/kserve-tryout/inference-config-patch-job.yaml
   ```

7. **Deploy a sample inference service** ([Reference](https://kserve.github.io/archive/0.15/get_started/first_isvc/))
   ```bash
   k create namespace kserve-test

   k apply -n kserve-test -f /home/esparig/projects/ai-inference-research/kserve-tryout/sklearn-iris.yaml
   ```

8. **Perform inference**
   ```bash
   SERVICE_HOSTNAME=$(k get inferenceservice sklearn-iris -n kserve-test -o jsonpath='{.status.url}' | cut -d "/" -f 3)

   curl -v -H "Host: ${SERVICE_HOSTNAME}"      -H "Content-Type: application/json"      http://confident-shtern7.im.grycap.net/v1/models/sklearn-iris:predict      -d @/home/esparig/projects/ai-inference-research/kserve-tryout/iris-input.json
   ```

9. **Run performance test**
   ```bash
   k create -f /home/esparig/projects/ai-inference-research/kserve-tryout/perf.yaml -n kserve-test
   ```

**Performance Test Results**

| Metric | Details | Values |
|--------|---------|--------|
| Requests | total, rate, throughput | 30000, 500.02, 500.01 |
| Duration | total, attack, wait | 59.999s, 59.998s, 1.24ms |
| Latencies | min, mean, 50, 90, 95, 99, max | 1.037ms, 1.489ms, 1.278ms, 1.565ms, 1.73ms, 4.502ms, 87.809ms |
| Bytes In | total, mean | 630000, 21.00 |
| Bytes Out | total, mean | 2460000, 82.00 |
| Success | ratio | 100.00% |
| Status Codes | code:count | 200:30000 |