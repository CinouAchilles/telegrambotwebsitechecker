FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# Install Chromium at build time (faster startup on Railway)
RUN python -m playwright install chromium

# Run your bot on container start
CMD ["python", "bot.py"]