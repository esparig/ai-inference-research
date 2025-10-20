
docker pull seldonio/mlserver:1.7.0

cd /tmp/mlserver-models/
mkdir -p /tmp/mlserver-models/my-model

vi model-setting.json
cd ~/projects/ai-inference-research/mlserver-locally/

uv venv mlserver-models
source mlserver-models/bin/activate
uv pip install scikit-learn joblib
python train.py
deactivate

docker run -p 8080:8080 -v /tmp/mlserver-models:/models seldonio/mlserver:1.

curl -X POST http://localhost:8080/v2/repository/models/my-model/load
  7 9ms    1m ago curl -X POST http://localhost:8080/v2/repository/index -d '{}'
  6 7ms    1m ago curl -X POST http://localhost:8080/v2/models/my-model/infer -d '{^J "inputs": [^J {^J "name": "input-0",^J "shape": [1],^J "datatype": "FP32",^J "data": [7]^J }^J ]^J}'
  5 12ms   1m ago curl -X POST http://localhost:8080/v2/models/my-model/infer -H "Content-Type: application/json" -d "{\"inputs\": [{\"name\": \"input-0\", \"shape\": [1], \"datatype\": \"FP32\", \"data\": [7]}]}"
  4 431us  1m ago cd my-model/
  3 87ms   1m ago car model.joblib
  2 1ms    1m ago cat model.joblib
  1 3ms   42s ago ll
  > 1ms   38s ago cat model-setting.json


## notes on youtube video
https://youtu.be/5tyLqAfW29I?si=K3ou0nZzM8WnxwKP

challenges:
- infrastructure usage -> manage costs
- dependency management -> manage dependencies all at one
- multiple ml frameworks -> unify how to serve
- standardize api definitions for inference
- capturing payload structures, give information in a clear way of how use the models
- handling versions of models

MLServer python based to serve ML modes
- support rest and grpc
- supports popular ml framsworks

How mlserver works:
- config for mlserver
- config for each model
- multi model serving (share resources, all models on the same container, they share resources)
- each infernce is processed by a python worker, maximizing use of cpu.
- serve models from hub (e.g. huggingface) 
- adaptative batching to reduce the number of requests and be able to attend them
- model deployment, consider seldon or kserve. 


