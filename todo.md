# TODO

### High 
- Fix 2nd pi node
    - Test failover handling, pod autoscaling, liveness/readiness probes
- Implement Prometheus + Grafana + tracing (OpenTelemetry or similar will allow seeing how long each DB call takes)
- Create architectural diagram
- Add LoadBalancer service option with MetalLB or similar
- Investigate Helm

### Medium
- Set up Pihole as a container
- Implement ELK stack
- Remove hardcoded default credentials and replace with env variables
- Terraform it and add cloud provisioning option
- How to address the revolving CSV data each month?
    - Zillow's download link changes frequently
    - Might have to modify my initContainer to be able to use python to scrape the link
    - Another alternative is automation pipeline to pull it to github repo
- Investigate ArgoCD
- Think about RBAC and network pols

### Low
- Use Helm charts to set up a dev/prod option
- GitHub Actions Pipeline for building images and deploying to pi nodes
- Alter docker-compose to use new multi-arch container and the stock mariadb container 
    - Same for ECS docs
    - I'm realizing that I'll have to reupload the import-data.sql file for docker-compose/ECS
- Improve front end 
    - Support endless table results
    - Include screenshots in the readme
- Kustomize to handle namespace better
- Contribute to Kompose to fix the bug you found with volume mount
