# TODO

### High 
- Test failover handling, pod autoscaling, liveness/readiness probes
- Implement Prometheus + Grafana + tracing (OpenTelemetry or similar will allow seeing how long each DB call takes)
- Create overarching architectural diagram
- Terraform it and add cloud provisioning option
    - Set up failover to EKS using Route 53 health checks and test it by turning off raspberry pis

### Medium
- Use Helm charts to create a distinct dev and prod? (this probably comes after I establish my monitoring solutions)
    - Each in different namespace, pod/svc/deployments differently named, use different container tags
    - Keep dev internal
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