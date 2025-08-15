# =====================
# 1️⃣ Base image
# =====================
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# =====================
# 2️⃣ Install dependencies
# =====================
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# =====================
# 3️⃣ Copy application code
# =====================
COPY . .

# =====================
# 4️⃣ Expose FastAPI port
# =====================
EXPOSE 8080

# =====================
# 5️⃣ Command to run app
# =====================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
