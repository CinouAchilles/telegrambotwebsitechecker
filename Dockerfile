FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

# Copy project
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser binaries (chromium)
RUN python -m playwright install chromium

CMD ["python", "bot.py"]