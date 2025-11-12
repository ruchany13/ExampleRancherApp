FROM python:3.13

RUN mkdir /app
WORKDIR /app

COPY ../parentinfo .
COPY ../requirements.txt .
COPY Docker/entrypoint-dev.sh .
COPY Docker/sample_data.json .
# Python buffers logs; this prevents that [behavior], enabling real-time monitoring of logs.
ENV PYTHONUNBUFFERED=1
# Prevents Python from compiling code to bytecode; this creates overhead for the additional container in a container architecture
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
RUN chmod +x entrypoint-dev.sh

ENTRYPOINT ["./entrypoint-dev.sh"]
# Development Enviroment
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]