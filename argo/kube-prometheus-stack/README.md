helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring -f values.yaml

helm upgrade prometheus prometheus-community/kube-prometheus-stack -n monitoring -f values.yaml
