# DevOps and Cloud Notes

## Containers
An image is an immutable build artifact; a container is a running instance. Prefer reproducible images, small attack surfaces, non-root execution where possible, and runtime configuration instead of embedded secrets.

## Kubernetes
Pods are scheduling units; Deployments manage replicas; Services provide stable networking; ConfigMaps/Secrets hold runtime configuration; Jobs/CronJobs handle finite work. Production also needs probes, resource limits, autoscaling, rolling updates, disruption controls, and observability.

## CI/CD and IaC
CI tests, lints, scans, and builds. CD promotes immutable artifacts. GitOps treats version-controlled configuration as desired state. Terraform describes infrastructure declaratively and maintains state that must be protected and reviewed.

## Cloud
Think in capabilities: compute, storage, database, networking, IAM, events, and observability. IAM follows least privilege. Managed AI and self-hosted inference differ in control, cost, latency, operations, and data handling.

## Practice
Containerize an API, write Kubernetes Deployment/Service manifests, create a test-build-scan-deploy pipeline, write minimal Terraform, and compare managed vs self-hosted inference.