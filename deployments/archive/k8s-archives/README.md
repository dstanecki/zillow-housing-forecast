### Zillow Housing Forecast K8s Archived Files 

I retired these files because of 2 major changes: 
1. I started baking my dbcreation script into my db pod rather than mounting it as shown here. I also removed the PVC configuration since I don't require persisting data right now, but I'm keeping the definition files in case I want to add it back.
2. I introduced Helm as the standard way to deploy the Zillow Housing Forecast app
