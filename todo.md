# TODO

### High 
- App starts 20s before database finishes initialization; need readiness probe or something
- Create Staging environment 
    - Leave ClusterIssuer OUT of Helm package and also for the dev use the different STAGING lets encrypt link
    - I need to variablize namespace (think about how to do it. If .Values.dev then namespace=zhf-dev? Otherwise zhf-prod?) for all template files 
    - I need to variabilize container latest tag (dev will use latest) 
    - I need to add zhf-dev.danielstanecki.com to Cloudflare and adjust R53 record and Ingress (the names v important here) 
    - Use Helper function to eliminate clutter   
        {{- define "zhf.domain" -}}
        {{- if eq .Values.environment "prod" }}zhf.danielstanecki.com{{ else }}zhf-dev.danielstanecki.com{{ end }}
        {{- end }}

- Implement Prometheus + Grafana + tracing (OpenTelemetry or similar will allow seeing how long each DB call takes)
    - Monitor SD card health to have warning signs before failure
- Terraform it and add cloud provisioning option
    - Set up failover to EKS using Route 53 health checks and test it by turning off raspberry pis

### Medium
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
- Alter docker-compose + ECS to use new containers
- Improve front end 
    - Support endless table results
    - Include screenshots in the readme
- Kustomize to handle namespace better
- Contribute to Kompose to fix the bug you found with volume mount
- Is Pihole worth it?