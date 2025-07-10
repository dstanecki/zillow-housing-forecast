# TODO

### High 
- Traefik still routes to dead nodes, need to add readinessProbes to app pod to mitigate
    - App starts 20s before database finishes initialization; need readiness probe on DB
- Update README, remove deploy steps and add screenshots
- Enable Flask monitoring (deploy svc monitor)
- Set up node export metrics and pod/container metrics with Prometheus 
- Implement Prometheus + Grafana
    - Monitor SD card health to have warning signs before failure
    - Secure dashboards (Prom + Grafana security concerns)
- Traefik dashboard?
- Implement tracing (OpenTel)

### Medium
- Terraform it and add cloud provisioning option
    - Set up failover to EKS using Route 53 health checks and test it by turning off raspberry pis
- Helmify app labels and selectors on servicemonitor.yaml, etc. 
- Email subscription (detect unusual swings in pricing predictions month-to-month)
- Create overarching architectural diagram once you have full EKS failover
- Implement ELK stack
- Remove hardcoded default credentials and replace with env variables
- How to address the revolving CSV data each month?
    - Zillow's download link changes frequently
    - CI/CD pipeline that pulls the latest data and programmatically alters SQL initialization script, then builds a new container, then k8s nodes pull container
- Investigate ArgoCD
- Think about RBAC and network pols

### Low
- Script to control RPi GPIO-4 fans
- Longhorn (not required for my read-only database but will be good to experiment in the future)
- Alter ECS to use new containers
- Kustomize to handle namespace better
- Contribute to Kompose to fix the bug you found with volume mount
