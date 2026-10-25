FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5003

WORKDIR /app
RUN useradd --system --uid 10001 --create-home appuser

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appuser app.py index.html general-questions.json cyber-questions.json institute-logo.svg ./

USER appuser
EXPOSE 5003
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-5003} --workers 2 --threads 4 --access-logfile - --error-logfile - app:app"]
