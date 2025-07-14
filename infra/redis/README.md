# Install redis from Helm chart using my custom values 
# Makes it more lightweight than the default installation and includes a service monitor
helm install my-redis bitnami/redis -n prod -f values.yaml
