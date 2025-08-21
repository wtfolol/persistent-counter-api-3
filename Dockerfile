FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create the data directory with proper permissions
RUN mkdir -p /data && \
    chmod 777 /data && \
    adduser -D myuser && \
    chown myuser:myuser /data

# Switch to non-root user for security
USER myuser

EXPOSE 5000

CMD ["python", "app.py"]
