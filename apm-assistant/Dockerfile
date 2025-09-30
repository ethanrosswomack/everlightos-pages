FROM python:3.11-slim
WORKDIR /app
# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
COPY proxy_app.py /app/proxy_app.py
COPY start.sh /app/start.sh
RUN pip install --no-cache-dir flask requests gunicorn || true
EXPOSE 8080 8081
CMD ["/app/start.sh"]
