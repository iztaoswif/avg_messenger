FROM python:3.12-slim

WORKDIR /app

COPY prod-requirements.txt .
RUN pip install --no-cache-dir -r prod-requirements.txt

COPY app/ ./app/
COPY static/ ./static/
COPY alembic/ ./alembic
COPY alembic.ini .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
