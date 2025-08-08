# TODO

### High 
- Establish and document in detail the most important metrics to monitor. I need to do internal monitoring in addition to external monitoring that I'm currently doing. 
	- Set up node export metrics and pod/container metrics with Prometheus 
		- Set up Prometheus alerts based on node RAM
- Think about when zhf can become official. Who is the target, what do they need, maybe provide a free tier and give the paid tier unlimited queries? 
- Address revolving CSV data (currently Actions pipeline curls csv and builds zhf-mariadb:latest once per month, but I would like to also automate k8s rollout)
    - Add a zhf-mariadb:v1.x.x build stage for prod
    - ArgoCD to handle automated rollout for dev, and manual approval for prod

### Medium
- Solution for aligning Redis cache with revolving data. (Actions workflow needs to trigger a redis clear on success)
- Venture into statefulness (e.g., add a dark mode switch and store that in user's browser cache)
- Monitor SD card health to have warning signs before failure
- Secure dashboards (Prom + Grafana security concerns)
- Traefik dashboard?
- Implement tracing (OpenTel)
- Helmify app labels and selectors on servicemonitor.yaml, etc. 
- Front end feature additions:
	- Map w/ color coded zip codes
	- Email subscription (detect unusual swings in pricing predictions month-to-month)
	- Printable PDFT reports (e.g., rank zip code forecasts per state/county)
	- Migration trends, crime, school rating trends, building permits
	- Compare ZIPs 
	- AI Chatbot (leaning away from this one though)
	- Days on Market (DOM average), inventory per zip, rent ratios
	- You want it to be an "insight". Home value insights? 
- Implement ELK stack
- Think about RBAC and network pols

### Low
- Script to control RPi GPIO-4 fans
- Longhorn (not required for my read-only database but will be good to experiment in the future)
- Contribute to Kompose to fix the bug you found with volume mount
