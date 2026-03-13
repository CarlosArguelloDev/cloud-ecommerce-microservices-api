FROM python:3.12-slim

RUN groupadd -r flask && useradd -r -g flask flask

WORKDIR /app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER flask

COPY --chown=flask . .

EXPOSE 5001

CMD ["gunicorn", "-b", "0.0.0.0:5001", "run:app"]
