# TODO

### High 
- Argo self manage
- Monitor uptime and start collecting uptime metrics with a goal target (e.g. 4 nines)
- Think about when zhf can become official. Who is the target, what do they need, maybe provide a free tier and give the paid tier unlimited queries? 
	- Does Flask support oauth and payments?
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
- Front end feature additions:
	- Email subscription (detect unusual swings in pricing predictions month-to-month)
	- Printable PDFT reports (e.g., rank zip code forecasts per state/county)
	- Migration trends, crime, school rating trends, building permits
	- Compare ZIPs 
	- AI Chatbot (leaning away from this one though)
	- Days on Market (DOM average), inventory per zip, rent ratios
	- You want it to be an "insight". Home value insights? 
- Create overarching architectural diagram once you have full EKS failover
- Implement ELK stack
- Think about RBAC and network pols
- Implement front end map (color coded zip codes)
- Make Terraform the primary method for other people to deploy the app (easier than the current bare metal setup)

### Low
- Script to control RPi GPIO-4 fans
- Longhorn (not required for my read-only database but will be good to experiment in the future)
- Contribute to Kompose to fix the bug you found with volume mount
