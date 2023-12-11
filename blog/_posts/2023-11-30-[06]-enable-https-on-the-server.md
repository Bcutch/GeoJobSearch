---
layout: post
category: K8s
---

In the final step of our setup, we secure our template website by enabling HTTPS using [Let's Encrypt](https://letsencrypt.org/getting-started/). Let's Encrypt provides certificates to websites, verifying their identity. To obtain a certificate, we need to demonstrate to Let's Encrypt that we have control over the domain hosting our website through the ACME protocol. Setting up this process on a Kubernetes (K8s) cluster is straightforward. Let's dive into it.

---
<h1 align="center">cert-manager</h1>
---

Cert-manager ([documentation](https://cert-manager.io/docs/)] is an open-source tool that creates ressources on a K8s cluster to help with the management and issuance of TLS (Transport Layer Security) certificates. The full guide on securing an NGINX-ingress controller can be found [here](https://cert-manager.io/docs/tutorials/acme/nginx-ingress/).

### Steps to setup HTTPS:

> Note: Ensure [Helm](https://helm.sh/docs/intro/install/) is installed on the host.

> Note: Confirm that the NGINX-ingress is already setup and that your website can be accessed using ```http```.

1. Create a cert-manager Issuer.

This can be added to the manifest.yaml file and pushed to the ```deploy``` branch or applied to the cluster directly using ```kubectl apply -f <filename>```:

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: letsencrypt-prod
  namespace: gitlab-agent-local
spec:
  acme:
    # The ACME server URL
    server: https://acme-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: example@email.com
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-prod
    # Enable the HTTP-01 challenge provider
    solvers:
    - http01:
        ingress:
          class: nginx
```

2. [Optional] Check the status of the issuer:

```
kubectl describe issuer letsencrypt-prod -n=gitlab-agent-local
```

The output should indicate that an ACME account was registered with the ACME server. If not, troubleshoot using this [guide](https://cert-manager.io/docs/troubleshooting/acme/).

3. Let's now edit the original ingress in **Blog 4** to use the certificate.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress
  namespace: gitlab-agent-local
  annotations:
    cert-manager.io/issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - amerch04.socs.uoguelph.ca		# Change the hostname
    secretName: template-tls
  rules:
  - host: amerch04.socs.uoguelph.ca	# Change the hostname
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

We have added two items to our ingress. We indicated it to use the letsencrypt-prod Issuer and added the tls spec (the secretName specified here is automatically created and used for HTTPS).