FROM python:3.11-slim

# Hugging Face Spaces runs the container as uid 1000 and needs a writable workdir.
RUN useradd -m -u 1000 user
WORKDIR /app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .

USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PORT=7860

# 7860 is the default HF Spaces port; Render overrides PORT to 10000.
EXPOSE 7860
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
