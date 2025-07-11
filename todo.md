# TODO

### High 
- Address revolving CSV data (currently Actions pipeline curls csv and builds zhf-mariadb:latest once per month, but I would like to also automate k8s rollout)
    - Add a zhf-mariadb:v1.x.x build stage for prod
    - ArgoCD to handle automated rollout for dev, and manual approval for prod
- Monitor Redis with Prometheus
- Set up Prometheus alerts based on node RAM and set in place a protocol to solve
- Traefik still routes to dead nodes, need to add readinessProbes to app pod to mitigate
    - App starts 20s before database finishes initialization; need readiness probe on DB
- Enable Flask monitoring (deploy svc monitor in prod)
- Set up node export metrics and pod/container metrics with Prometheus 

### Medium
- Monitor SD card health to have warning signs before failure
- Secure dashboards (Prom + Grafana security concerns)
- Traefik dashboard?
- Implement tracing (OpenTel)
- Terraform it and add cloud provisioning option
    - Set up failover to EKS using Route 53 health checks and test it by turning off raspberry pis
- Helmify app labels and selectors on servicemonitor.yaml, etc. 
- Email subscription (detect unusual swings in pricing predictions month-to-month)
- Create overarching architectural diagram once you have full EKS failover
- Implement ELK stack
- Think about RBAC and network pols

### Low
- Script to control RPi GPIO-4 fans
- Longhorn (not required for my read-only database but will be good to experiment in the future)
- Alter ECS to use new containers
- Kustomize to handle namespace better
- Contribute to Kompose to fix the bug you found with volume mount
