FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app
COPY . /app

# Install Python dependencies only
RUN pip install --no-cache-dir -r requirements.txt

# Start your bot
CMD ["python", "bot.py"]