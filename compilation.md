# Emerging Trends in the Cloud-native Ecosystem: Cloud Native Powers AI

https://www.cncf.io/blog/2024/11/19/emerging-trends-in-the-cloud-native-ecosystem/

Since 2016, OpenAI, a pioneer in the industry, has been running its training and inference workloads on Kubernetes [7]. It has pushed the limits of platform technology by running clusters with up to 2500 nodes. All the advantages of cloud-native technologies and platforms such as scalability and dynamic nature transfer directly to artificial intelligence (AI) workloads. This is especially true for large language models (LLMs), a fast-moving area of AI technology that is transforming every industry it touches. The trend within the cloud-native landscape to cater to AI training and services is spread across the LF AI & Data and the CNCF foundations [8]. CNCF has also developed and published a cloud-native AI landscape along with a white paper earlier this year [9, 10]. 

LF AI & Data and CNCF house open-source projects that are critical building blocks for the AI revolution. These include projects such as:

OPEA, a collection of cloud-native patterns for GenAI workloads [11]
Milvus, a high-performance vector database [12]
Kubeflow, a project to deploy machine-learning workflows on Kubernetes [13]
KServe, a toolset for serving predictive and generative machine-learning models [14]
Apart from projects, there are also foundational improvements and changes being made to Kubernetes such as the elastic indexed job to better handle the demands of AI workloads [15]. Considerable thought leadership in this space is being driven by the members of the cloud-native AI working group under the Technical Advisory Group for Runtime (TAG-Runtime) of CNCF [16].

Companies experimenting with AI typically start with a proprietary SaaS or cloud offering. They can further expand their reach into cloud-native AI by setting up and running open-source projects such as KServe to experiment with open-source LLMs. The ability to curate and self-host LLMs is the first step to addressing privacy, security, and regulatory concerns with proprietary offerings and developing in-house capabilities in this area.

[7] https://kubernetes.io/case-studies/openai/ 

[8] https://lfaidata.foundation/ 

[9] https://landscape.cncf.io/?group=cnai 

[10] https://www.cncf.io/reports/cloud-native-artificial-intelligence-whitepaper/ 

[11] https://opea.dev/

[12] https://milvus.io/

[13] https://kserve.github.io/website/latest/

[14] https://www.kubeflow.org/ 

[15] https://github.com/kubernetes/enhancements/tree/master/keps/sig-apps/3715-elastic-indexed-job#summary 

[16] https://tag-runtime.cncf.io/wgs/cnaiwg/ 

# Cloud Native Artificial Intelligence Whitepaper

https://www.cncf.io/wp-content/uploads/2024/03/cloud_native_ai24_031424a-2.pdf

## Model Serving
Model serving differs chiefly from data processing and training because of load variability and often latency requirements. Further, there are considerations of service resiliency in addition to sharing infrastructure to reduce costs. Also, AI model characteristics are distinct, varying significantly across classical ML, Deep Learning (DL), Generative AI (GAI) LLMs, and, more recently, the multi-modal approaches (e.g., text to video). Different workloads necessitate varied support from ML infrastructure. 
For example, before the emergence of LLMs, model serving typically required only a single GPU. Some users opted for CPU-based inference if the workloads were not latency-sensitive. However, when serving LLMs, the performance bottleneck shifts from being compute-bound to memory-bound due to the autoregressive nature of the Transformer decoder.[46]

## Microservice Architecture and Developer Experience
CN is based on microservice architecture. However, this may pose a challenge for AI, dealing with each stage in the ML pipeline as a separate microservice. Many components may make maintaining and synchronizing their outputs and hand-offs challenging. Even if users only want to play with these solutions on their laptops, they might still need to create tens of Pods. The complexity makes the infrastructure lack the flexibility to adapt to versatile ML workloads.
Second, the microservice-based ML infrastructure leads to a fragmented user experience. For example, in their daily workflows, AI Practitioners may need to build container images, write custom resource YAML files, use workflow orchestrators, and so on instead of focusing solely on their ML Python scripts. This complexity also manifests as a steeper learning curve, requiring users to learn many systems outside their expertise and/or interest. Third, the cost increases significantly when integrating each stage from different systems in the ML model lifecycle. The Samsara engineering blog [47] mentions that its ML production pipelines were hosted across several microservices with separate data processing, model inference, and business logic steps. Split infrastructure involved complex management to synchronize resources, slowing the speed of development and model releases. Then, using Ray, Samsara built a unified ML platform that enhanced their production ML pipeline performance, delivering nearly a 50% reduction in total yearly ML inferencing costs for the company, stemming chiefly from resource sharing and eliminating serialization and deserialization across stages. These issues highlight the need for a unified ML infrastructure based on a general-purpose distributed computation engine like Ray. Ray can supplement the existing Cloud Native ecosystem, focusing on computation, allowing the Cloud Native ecosystem to concentrate on deployment and delivery. The Ray/KubeRay community has collaborated extensively with multiple Cloud Native communities, such as Kubeflow [48], Kueue [49], Google GKE [50], and OpenShift [51].

## Model Placement
Users ideally like to deploy multiple, possibly unrelated, models for inference in a single cluster while also seeking to share the inference framework to reduce costs and obtain model isolation. Further, for resiliency, they want replicas in different failure zones. Kubernetes provides affinity and anti-affinity mechanisms to schedule workloads in different topology domains (e.g., zone, node)[52], but usability improvements can help users take advantage of these features. Resource Allocation Model serving requires handling, chiefly, the model parameters. The number of parameters and the representation size indicate the memory needed. Unless dealing with a trillion parameter LLM, these typically require only a portion of a GPU. This highlights the need to be able to fractionalize expensive accelerators like GPUs. The DRA project, [53] which is still in alpha, seeks to make GPU scheduling more flexible. Another consideration is response latency, which depends significantly on the use case. For instance, the response latency desired to detect objects on the road in an autonomous driving context is several orders lower than tolerable while creating an image or writing a poem. Additional serving instances may need to be launched for low-latency applications under high-load conditions. These could land on a CPU, GPU, or other computing resource if the desired latency can be honored. Support for such cascading opportunistic scheduling on available resources is still evolving in Kubernetes.

Further, event-driven hosting is ideal for not wasting resources and keeping costs down. The Kubernetes Event Driven Autoscaling (KEDA) [54] project is well-suited here, provided the model loading latency is tolerable to still deliver on the end-to-end service latency. An opportunity here is to provide better support for model sharing by delivering models in an Open Container Initiative [55] (OCI) format, an immutable file system that lends itself to sharing. Another solution is to use AI for CN, in particular, to predict use and proactively float or shut down serving instances to handle the expected load.

[46] https://arxiv.org/abs/1706.03762
[47] https://www.samsara.com/blog/building-a-modern-machine-learning-platform-with-ray
[53] https://kubernetes.io/docs/concepts/scheduling-eviction/dynamic-resource-allocation/

