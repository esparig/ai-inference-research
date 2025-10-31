# KServe Installation (Serverless) and Tryout Guide

1. **Install KServe (from cluster front-end node)**
   ```bash
   sudo helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd --version v0.15.0
   ```

2. **Install KServe Resources in Serverless mode**
   ```bash
   k create namespace kserve

   # From cluster front-end node
   sudo helm install kserve oci://ghcr.io/kserve/charts/kserve --version v0.15.0  --namespace kserve --create-namespace --set kserve.controller.deploymentMode=Serverless 
   ```


3. **Crear DNS record**

   ```
   *.<random-domain>.alu.cursocloudaws.net → <IP>
   ```


4. **Configure Knative Domain Mapping**

   ```bash
   kubectl edit configmap config-domain -n knative-serving
   ```

   Add:
   
   ```yaml
   data:
     <random-domain>.alu.cursocloudaws.net: ""
   ```

   Check that the new value is added:
   ```bash
   kubectl get configmap config-domain -n knative-serving -o jsonpath="{.data}" | jq keys
   ```


5. **Disable Istio top level virtual host**

   Edit inferenceservice-config configmap:

   ```bash
   kubectl edit configmap/inferenceservice-config --namespace kserve
   ```

   Add the flag `"disableIstioVirtualHost": true` under the ingress section:

   ```yaml
   ingress : |- {
     "disableIstioVirtualHost": true
   }
   ```

   Restart the KServe Controller
   ```bash
   kubectl rollout restart deployment kserve-controller-manager -n kserve
   ```


6. **Expose Kourier to the Outside**

   ```bash
   kubectl edit svc kourier -n kourier-system
   ```

   Change the type to NodePort:
   ```yaml
   spec:
     type: NodePort
   ```

   Verify that Kourier is exposed via NodePort
   
   ```bash
   kubectl get svc -n kourier-system
   ```
   
   Open the following port in your OpenStack VM firewall/security group to allow external access:
   
   ```bash
   kubectl get svc kourier -n kourier-system -o jsonpath="{.spec.ports[?(@.name=='http2')].nodePort}"
   ```
   

7. **Deploy a sample inference service** ([Reference](https://kserve.github.io/archive/0.15/get_started/first_isvc/))
   
   Create a namespace and deploy the sample PMML model:

   ```bash
   kubectl create namespace kserve-test

   kubectl apply -n kserve-test -f ./kserve-tryout/pmml.yaml

   # Check the KServe inference service is created and the URL is assigned:
   kubectl get ksvc -n kserve-test
   ```


8. **Perform inference**
   
   ```bash
   # Replace EXTERNAL_DOMAIN and KOURIER_NODE_{IP,PORT} with your values
   curl -v \
     -H "Host: pmml-demo-predictor.kserve-test.EXTERNAL_DOMAIN" \
     -H "Content-Type: application/json" \
     "http://<KOURIER_NODE_IP>:<KOURIER_NODE_PORT>/v1/models/pmml-demo:predict" \
     -d @./kserve-tryout/pmml-input.json
   ```


9. **Run performance test**

   Deploy sklearn-iris inference service if not already done:

   ```bash
   kubectl create -f ./kserve-tryout/sklearn-iris.yaml -n kserve-test
   ```

   Run performance test:
   
   ```bash
   kubectl create -f ./kserve-tryout/perf.yaml -n kserve-test
   ```

   Get performance test results:
   
   ```bash
   # Find the perf pod first, then show logs
   kubectl get pods -n kserve-test
   # Example:
   # PERF_POD=$(kubectl get pods -n kserve-test -l app=perf -o jsonpath='{.items[0].metadata.name}')
   # kubectl logs "${PERF_POD}" -n kserve-test
   ```

   **Performance Test Results**

   | Metric | Details | Values |
   |-------:|:--------|:------|
   | Requests | total, rate, throughput | 30000, 500.02, 500.00 |
   | Duration | total, attack, wait | 1m0s, 59.998s, 2.181ms |
   | Latencies | min, mean, 50, 90, 95, 99, max | 1.917ms, 2.569ms, 2.346ms, 3.055ms, 3.552ms, 5.564ms, 61.471ms |
   | Bytes In | total, mean | 630000, 21.00 |
   | Bytes Out | total, mean | 2460000, 82.00 |
   | Success | ratio | 100.00% |
   | Status Codes | code:count | 200:30000 |
   | Error Set | | (none) |


````

