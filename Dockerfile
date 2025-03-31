# Use the official Prometheus base image
FROM prom/prometheus:latest

# Set the working directory
WORKDIR /etc/prometheus

# Copy the Prometheus configuration file
COPY prometheus.yml /etc/prometheus/prometheus.yml

# Expose Prometheus default port
EXPOSE 9090

# Start Prometheus
CMD ["--config.file=/etc/prometheus/prometheus.yml"]