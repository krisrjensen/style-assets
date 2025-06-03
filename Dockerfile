# Style Assets Server Dockerfile
# Optimized for asset management and file serving

FROM python:3.9-slim as builder

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.9-slim

WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/app/.local

# Copy application code
COPY . .

# Create directories for asset storage
RUN mkdir -p fonts color_schemes templates bundles && \
    chown -R app:app /app

# Switch to non-root user
USER app

# Make sure scripts are in PATH
ENV PATH=/home/app/.local/bin:$PATH

# Expose port
EXPOSE 5003

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5003/health', timeout=5)"

# Run the application
CMD ["python", "app.py"]