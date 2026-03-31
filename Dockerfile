FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install chromium

COPY . /app

CMD ["python", "bot.py"]