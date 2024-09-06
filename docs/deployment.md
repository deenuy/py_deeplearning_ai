# Deploying on OpenShift

This guide will walk you through the process of deploying the Logistic Regression Image Classifier on OpenShift.

## Prerequisites

Before you begin, ensure you have:

1. OpenShift CLI (`oc`) installed and configured
2. Access to an OpenShift cluster
3. Docker installed on your local machine
4. Your project's Docker image built and pushed to a container registry

## Step 1: Log in to OpenShift

Open a terminal and log in to your OpenShift cluster:

```bash
oc login <your-openshift-cluster-url>
```

### Step 2: Create a New Project
Create a new project in OpenShift:
```bash
oc new-project logistic-regression-classifier
```

### Step 3: Create a Deployment Configuration
Create a new file named deployment.yaml with the following content:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: logistic-regression-classifier
spec:
  replicas: 1
  selector:
    matchLabels:
      app: logistic-regression-classifier
  template:
    metadata:
      labels:
        app: logistic-regression-classifier
    spec:
      containers:
      - name: logistic-regression-classifier
        image: <your-docker-image>:<tag>
        ports:
        - containerPort: 8000
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "200m"
            memory: "256Mi"
```

Replace <your-docker-image> and <tag> with your Docker image details.

### Step 4: Apply the Deployment Configuration
Apply the deployment configuration:
```bash
oc apply -f deployment.yaml
```

### Step 5: Create a Service
Create a service to expose your application:
```bash
oc expose deployment logistic-regression-classifier --port=8000
```

### Step 6: Create a Route
Create a route to make your application accessible from outside the cluster:
```oc expose service logistic-regression-classifier
```

### Step 7: Verify the Deployment
Check the status of your deployment:
```bash
oc get pods
oc get services
oc get routes
```

### Step 8: Access Your Application
Get the URL of your application:
```
oc get route logistic-regression-classifier
```

You can now access your application using this URL.

## Updating Your Deployment
To update your deployment with a new version of your application:

Build and push a new version of your Docker image
Update the image in your deployment:

```bash
oc set image deployment/logistic-regression-classifier logistic-regression-classifier=<your-docker-image>:<new-tag>
```

## Scaling Your Application
To scale your application, you can modify the number of replicas:
```bash
oc scale deployment logistic-regression-classifier --replicas=3
```

## Monitoring and Logs
To view logs for your application:
```bash
oc logs deployment/logistic-regression-classifier
```

For real-time logs:
```bash
oc logs -f deployment/logistic-regression-classifier
```

## Troubleshooting
If you encounter issues:

```bash
# Check pod status: 
oc get pods
# Describe the pod for more details: 
oc describe pod <pod-name>
# Check pod logs: 
oc logs <pod-name>
```

## Cleaning Up
To remove your application from OpenShift:
```bash
oc delete all -l app=logistic-regression-classifier
oc delete project logistic-regression-classifier
```

## Additional Resources

- OpenShift Documentation
- Kubernetes Documentation