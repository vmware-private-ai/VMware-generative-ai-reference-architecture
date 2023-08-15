#  Serving LLMs using vLLM deployed on Ray Serve.

### The scripts are based on the examples provided by the [Anyscale](https://www.anyscale.com/blog/continuous-batching-llm-inference) and [vLLM](https://github.com/vllm-project/vllm/tree/main/examples) teams.

## Requirements.

- First you need to have a Kubernetes (K8s) cluster up and running.
- The K8s cluster must be equipped with NVIDIA GPUs with compute capabilities >= 7.0
- If you're using VMware Tanzu Kubernetes, you can check this documentation to learn <br> how to enable [GPUs on Tanzu Kubbernetes](https://docs.vmware.com/en/VMware-Tanzu-Kubernetes-Grid/1.6/vmware-tanzu-kubernetes-grid-16/GUID-tanzu-k8s-clusters-hardware.html).
- The AnyScale team provides comprehensive documentation about Ray Serve and how to deploy it K8s<br>
using Kuberay. Follow the [Ray Serve](https://docs.ray.io/en/latest/serve/index.html) documentation to learn how to customize<br>the vLLM service deployment on Ray Serve beyond the scope of this guide.


## Deploying a vLLM service on Ray Serve.
- Set `ClusterRoleBinding` to let Kuberay run privileged types of workloads.<br>
```
kubectl create clusterrolebinding default-tkg-admin-privileged-binding \
--clusterrole=psp:vmware-system-privileged --group=system:authenticated
```
- Ensure you have [Helm installed](https://helm.sh/docs/intro/install/) in your environment.
- Deploy Kuberay in your K8s cluster. More details at [KubeRay Operator install docs](https://github.com/ray-project/kuberay/blob/master/helm-chart/kuberay-operator/README.md)

- Add the Kuberay Helm repo.
````
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
````

- Install both CRDs and KubeRay operator v0.6.0.
````
helm install kuberay-operator kuberay/kuberay-operator --version 0.6.0

# NAME: kuberay-operator
# LAST DEPLOYED: Thu Aug 10 12:41:07 2023
# NAMESPACE: default
# STATUS: deployed
# REVISION: 1
# TEST SUITE: None
````

- Check the KubeRay operator pod in the `default` namespace.
````
kubectl get pods

# NAME                                READY   STATUS    RESTARTS   AGE
# kuberay-operator-6b68b5b49d-jppm7   1/1     Running   0          6m40s
````
- Pull the ray-service.vllm.yaml manifest (from this repo) from the GitHub repo raw URL.
```` 
wget -L https://raw.githubusercontent.com/vecorro/vllm_examples/main/ray-service.vllm.yaml
````
- Create a Ray Serve cluster using the manifest
````
kubectl apply -f ray-service.vllm.yaml
````
- Verify the Ray cluster pods got created
````
kubectl get pods

# The Ray cluster starts to create the head and worker pods
# NAME                                           READY   STATUS              RESTARTS   AGE
# kuberay-operator-6b68b5b49d-jppm7              1/1     Running             0          23m
# vllm-raycluster-c9wk4-head-gw958               0/1     ContainerCreating   0          67s
# vllm-raycluster-c9wk4-worker-gpu-group-wl7k2   0/1     Init:0/1            0          67s
````
- After several minutes, the Ray cluster should be up and running
````
kubectl get pods

# NAME                                           READY   STATUS    RESTARTS   AGE
# kuberay-operator-6b68b5b49d-jppm7              1/1     Running   0          39m
# vllm-raycluster-c9wk4-head-gw958               1/1     Running   0          17m
# vllm-raycluster-c9wk4-worker-gpu-group-wl7k2   1/1     Running   0          17m
````
- The vLLM service will get exposed as a LoadBalancer. In this example the vLLM API service (vllm-serve-svc)<br>gets exposed over http://172.29.214.16:8000. That is the URL you need to use to make prompt completion requests.
````
 kubectl get svc
 
# NAME                             TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)
# kuberay-operator                 ClusterIP      10.105.14.110    <none>          8080/TCP
# vllm-head-svc                    LoadBalancer   10.100.208.111   172.29.214.17   10001:32103/TCP,8265:32233/TCP... 
# vllm-raycluster-c9wk4-head-svc   LoadBalancer   10.103.27.23     172.29.214.16   10001:30474/TCP,8265:30563/TCP...
# vllm-serve-svc                   LoadBalancer   10.104.242.187   172.29.214.18   8000:30653/TCP...

````
- You can use the `vllm-raycluster-c9wk4-head-svc` IP on port 8265 (http://172.29.214.16:8265) to access the<br>
Ray cluster dashboard to monitor the Ray cluster status and activity.


- The `ray-service.vllm.yaml` manifest has a section that defines the vLLM service deployment:
````
spec:
  serviceUnhealthySecondThreshold: 3600 # Config for the health check threshold for service. Default value is 60.
  deploymentUnhealthySecondThreshold: 3600 # Config for the health check threshold for deployments. Default value is 60.
  serveConfigV2: |
    applications:
      - name: vllm
        import_path: vllm_falcon_7b:deployment
        runtime_env:
          working_dir: "https://github.com/vecorro/vllm_examples/archive/refs/heads/main.zip"
          pip: ["vllm==0.1.3"]
````
- Here some remarks about the service definition:
    - We increased `serviceUnhealthySecondThreshold` and `deploymentUnhealthySecondThreshold`to give Ray sufficient time <br>
  to install vLLM on a virtual working environment. The vLLM service can take >15 minutes to install mainly because<br>
  downloading an LLM from the Hugging Face repo could take a long time.
    - `working_dir`is set to the URL of the compressed version of this Github repo. Ray will use this URL to pull the<br>
  Python code that implements the vLLM service.
    - We use vLLM 0.1.3 to create the Ray working env.
    - `import_path` is set to the proper `module:object` for Ray Serve to get the service definition. In this case <br>
  the `module` is the `vllm_falcon_7b.py` Python script and `deployment` is a `serve.deployment.bind()`<br>
  object type defined inside that script.


- Next you can run the `gradio_webserver.py` script to serve prompt completions from a web UI. You need to have<br>
the [Gradio](https://www.gradio.app/) Python package installed to run the web UI. To install it, run :
```
pip install gradio
```
- Now you can run the `gradio_webserver.py` by replacing the `--model-url` value with the hostname or<br>
the IP address of `vllm-serve-svc` pod. Example:
````
python gradio_webserver.py --model-url="http://172.29.214.18:8000"
````
- Then you may open URL `http://localhost:8001` from your web browser and the Gradio web interface will<br> 
give you a chat window to interact with the LLM.
