---
layout: post
category: K8s
---

In the previous post, we set up a local application using Minikube, leveraging the features of Kubernetes (K8s). In this post, our focus shifts to the deployment of the Spring template on this host using Kubernetes. The key elements we'll explore include creating deployments, services, and ingress, all important components for deploying our application. Continuous integration and deployment will be discussed in the following post.

---
<h1 align="center">Overview</h1>
---

Let's begin by examining the diagram below to understand the structure of our Kubernetes cluster:

![Kube-manifest]({{site.baseurl}}/assets/img/kube-manifest.png)

All Kubernetes manifest files are located in the ```/k8s/``` folder and create objects within the gitlab-agent-local namespace (note: the namespace can be customized).


---
<h1 align="center">Secret</h1>
---

Similar to the previous post, we're retrieving images from a remote repository to run in the pods. However, this time, the repository is private, which requires a token for image pulling. The Gitlab Container Registry serves as our image storage, and conveniently, it allows us create tokens and use them as secrets for pulling our images.

### Pushing Images to Gitlab Container Registry (Full guide can be found [here](https://docs.gitlab.com/ee/user/packages/container_registry/))

- **Authentication:**

Before pushing images, let's create an access token. In this tutorial, we'll use a project access token. Follow these steps:

1. On the left sidebar within your project, Select **Settings**
2. Look for **Access Tokens**
3. Create a new access token with a name, desired expiration data, role, and with the **api** scope (Choose whatever fits your needs)
4. Save the token generated

Now that we have an access token, log into Docker with your access token using the following command:

```
docker login registry.example.com -u <username> -p <token>
```

- **Build and Push Images:**

Once logged in, navigate to the directory with the Dockerfile and run the following commands:

```
docker build -t registry.example.com/project/image:tag .
docker push registry.example.com/project/image:tag
```

### Creating a secret with our token to use in our K8s cluster

You can use the same token created earlier, or you can create a new one to build our k8s secret. There are different [methods](https://kubernetes.io/docs/concepts/configuration/secret/) to create a secret, but in this case, we'll be creating a serialized Docker config file with our token. Follow these steps to create your secret manifest file:

1. Create a docker config file named 'config.json'

```json
{
 	"auths": {
		"registry.socs.uoguelph.ca": {
      			"username": "user",
      			"password": "token"
    		}
	}
}
```

2. Encode file by running

```
base64 config.json
```

3. Create your secret.yaml manifest file

```yaml
apiVersion: v1
data:
  .dockerconfigjson: <base64 encoded config.json string>
kind: Secret
metadata:
  name: regcred
  namespace: gitlab-agent-local
type: kubernetes.io/dockerconfigjson
```

4. Apply your secret manifest

```
kubectl apply -f secret.yaml
```

In the next section, we'll refer to the ```regcred``` secret we created when setting up our deployment.


---
<h1 align="center">Deployments</h1>
---

Let's examine the deployment manifest files for each app. These are similar to what we built in the previous post for the JavaScript applications. We are also using the same environment variables as those in our Docker Compose.yaml file. The service addresses, just like in the Compose file, use the service name as the host instead of localhost. The services created in the next section are named as follows: **react-service**, **spring-service**, and **sql-service**. The **regcred** secret is added under the **imagePullSecrets** specification.

### Spring deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spring-deployment
  namespace: gitlab-agent-local
  labels:
    app: spring
spec:
  replicas: 2
  selector:
    matchLabels:
      app: spring
  template:
    metadata:
      labels:
        app: spring
    spec:
      containers:
      - name: spring
        image: registry.socs.uoguelph.ca/amerch04/springtemplate/spring:v0.0.0
        imagePullPolicy: Always
        env:
          - name: DB_ADDRESS
            value: jdbc:mysql://mysql-service:3306
          - name: DB_DATABASE
            value: template_db
          - name: DB_USER
            value: root
          - name: DB_PASSWORD
            value: pwd
      imagePullSecrets:		# Specify the secret to use
      - name : regcred
```

### Mysql deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-deployment
  namespace: gitlab-agent-local
  labels:
    app: mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: registry.socs.uoguelph.ca/amerch04/springtemplate/mysql:v0.0.0
        imagePullPolicy: Always
        env:
          - name: MYSQL_ROOT_PASSWORD
            value: pwd
          - name: MYSQL_DATABASE
            value: template_db
        ports:
        - containerPort: 3360
      imagePullSecrets:
      - name : regcred
```

### React deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: react-deployment
  namespace: gitlab-agent-local
  labels:
    app: react
spec:
  replicas: 2
  selector:
    matchLabels:
      app: react
  template:
    metadata:
      labels:
        app: react
    spec:
      containers:
      - name: react
        image: registry.socs.uoguelph.ca/amerch04/springtemplate/react:v0.0.0
        imagePullPolicy: Always
        env:
          - name: BACKEND_PROXY
            value: http://spring-service:8080
      imagePullSecrets:
      - name : regcred
```

All the deployment created can be applied to the cluster using the ```kubectl apply -f <filename>``` command.

---
<h1 align="center">Services</h1>
---

Creating services is a straightforward process. Let's outline how to create one for each deployment. Each service port maps to the port where our service is hosted. Below is the YAML file content, with each service separated by ---:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: spring-service
  namespace: gitlab-agent-local
spec:
  selector:
    app: spring
  ports:
  - port: 8080
    targetPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: react-service
  namespace: gitlab-agent-local
spec:
  selector:
    app: react
  ports:
  - port: 3000
    targetPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
  namespace: gitlab-agent-local
spec:
  selector:
    app: mysql
  ports:
  - port: 3306
    targetPort: 3306
```

Once again, this can be applied using the ```kubectl apply -f <filename>``` command.

---
<h1 align="center">Ingress</h1>
---

In the previous post, when setting up our local Minikube cluster, we enabled the ```ingress addon```. On the host where our app is deployed, the nginx-ingress controller is preinstalled. If you don't have it, follow the instructions on this [page](https://kubernetes.github.io/ingress-nginx/deploy/) to set it up.

Here is our ingress yaml file:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress
  namespace: gitlab-agent-local
spec:
  rules:
  - host: amerch04.socs.uoguelph.ca	# Replace with your host address
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: react-service
            port: 
              number: 3000
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: spring-service
            port: 
              number: 8080
```

Apply the ingress using ```kubectl apply -f <filename>``` comand.

If your host is setup to expose it's ip address with port 80, you should be able to access the app on your host's address. In our case, that is ```amerch04.socs.uoguelph.ca```.
