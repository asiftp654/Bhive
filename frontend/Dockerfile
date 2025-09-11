# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy frontend files
COPY index.html .
COPY styles.css .
COPY api.js .
COPY auth.js .
COPY investments.js .
COPY main.js .

# Expose port 8080
EXPOSE 8080

# Add labels for better organization
LABEL maintainer="Bhive MF Team"
LABEL description="Frontend for Bhive Mutual Fund Application"
LABEL version="1.0.0"

# Start simple HTTP server
CMD ["python", "-m", "http.server", "8080"]
