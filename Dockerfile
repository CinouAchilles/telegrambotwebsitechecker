FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

COPY requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . /app

# Ensure browsers are installed (safety step)
RUN python -m playwright install

CMD ["python", "bot.py"]