FROM python:3.12-slim
RUN pip install Flask
WORKDIR /app
COPY app.py .
ENV FLAG="flag{sqli_filtered}"
EXPOSE 5000
CMD ["python", "app.py"]
