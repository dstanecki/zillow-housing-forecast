# Helm upgrade commands

# Prod
helm upgrade prod -n prod zhf-chart-0.1.0.tgz -f zhf-chart/values-prod.yaml

# Dev
helm upgrade dev -n dev zhf-chart-0.1.0.tgz -f zhf-chart/values-dev.yaml

