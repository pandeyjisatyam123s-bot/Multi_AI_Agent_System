# Stage 1: Build the React frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/web
# Copy web package files
COPY web/package*.json ./
RUN npm install
# Copy web source
COPY web/ ./
RUN npm run build

# Stage 2: Build the Python backend
FROM python:3.10-slim
WORKDIR /app

# Install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY . .

# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/web/dist ./web/dist

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
