FROM python:3.10.5-slim-buster as base
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt ./
RUN /opt/venv/bin/python3 -m pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir 

FROM python:3.10.5-slim-buster as build
COPY --from=base /opt/venv /opt/venv
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /code
COPY . /code
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]