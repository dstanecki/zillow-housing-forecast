# TODO

### Mission
Address the time-poorness of real estate agents by providing a centralized point of zip-level data insights. Stand out from the competition by focusing on this single niche and providing unparalleled ease of use. 

### High 
- Add oauth secret to Terraform code + github secrets
- Heatmap toggling, performance improvements
- Need Longhorn for HA across nodes
- Before enabling db writes, e.g. google users being written to db, need a at minimum nightly backup solution to the cloud that works with my GKE failover
- Implement tracing (OpenTel and Tempo) and logging (Alloy and Loki)
- Implement confidence band

### Medium
- Solution for aligning Redis cache with revolving data. (Actions workflow needs to trigger a redis clear on success)
- Monitor SD card health to have warning signs before failure
- Secure dashboards (Prom + Grafana security concerns)
- Traefik dashboard?
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
- Think about RBAC and network pols

### Low
- Script to control RPi GPIO-4 fans
- Longhorn (not required for my read-only database but will be good to experiment in the future)
- Contribute to Kompose to fix the bug you found with volume mount

