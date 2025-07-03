# Build multi-arch container and push

docker buildx build --platform linux/amd64,linux/arm64 -t dstanecki/zhf:latest -f Dockerfile . --push
