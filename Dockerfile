FROM python:3.10.4

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY ./scripts/entrypoint.sh .
ENTRYPOINT ["sh", "entrypoint.sh"]

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm -f requirements.txt

COPY ./shopping_cart_api .