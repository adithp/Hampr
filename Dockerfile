# 1. Base Python image
FROM python:3.11-slim

# 2. Do not generate .pyc files and allow print without buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Create working directory inside container
WORKDIR /app

# 4. Copy project files into container
COPY ./src/hampr /app/

# 5. Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Default command (start Django server)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
