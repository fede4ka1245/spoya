# Use a base Python image
FROM python:3.11
WORKDIR /app

COPY /back .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "python", "main.py" ]