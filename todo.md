# TODO

### High 
- ApplicationSet for dev/prod argo apps
- Monitor uptime and classify it as 99.9%, etc
- Dedicate all high-write components to SSD node
- Solution for aligning Redis cache with revolving data. (Actions workflow needs to trigger a redis clear on success)
- Decide on how to handle kube-prometheus-stack (argocd giving me problems)
- Finish the GKE pipeline
- Address revolving CSV data (currently Actions pipeline curls csv and builds zhf-mariadb:latest once per month, but I would like to also automate k8s rollout)
    - Add a zhf-mariadb:v1.x.x build stage for prod
    - ArgoCD to handle automated rollout for dev, and manual approval for prod
- Set up Prometheus alerts based on node RAM and set in place a protocol to solve
- Set up node export metrics and pod/container metrics with Prometheus 

### Medium
- Monitor SD card health to have warning signs before failure
- Secure dashboards (Prom + Grafana security concerns)
- Traefik dashboard?
- Implement tracing (OpenTel)
- Helmify app labels and selectors on servicemonitor.yaml, etc. 
- Email subscription (detect unusual swings in pricing predictions month-to-month)
- Create overarching architectural diagram once you have full EKS failover
- Implement ELK stack
- Think about RBAC and network pols
- Implement front end map (color coded zip codes)
- Make Terraform the primary method for other people to deploy the app (easier than the current bare metal setup)

### Low
- Script to control RPi GPIO-4 fans
- Longhorn (not required for my read-only database but will be good to experiment in the future)
- Contribute to Kompose to fix the bug you found with volume mount
