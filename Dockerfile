FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-java-common \
    default-jre \
    python3 \
    python3-pip \
    python3-uno \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-noto-cjk \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install HWP to DOCX/PDF LibreOffice extension
RUN wget -O /tmp/H2Orestart.oxt https://github.com/ebandal/H2Orestart/releases/download/v0.7.4/H2Orestart.oxt && \
    libreoffice --headless --accept="socket,host=0.0.0.0,port=2002;urp;" --nofirststartwizard & \
    sleep 5 && \
    unopkg add --shared /tmp/H2Orestart.oxt

WORKDIR /app
RUN adduser --disabled-password --gecos '' --uid 1234 appuser
RUN mkdir -p /tmp/libreoffice && \
    chown -R appuser:appuser /app && \
    chown -R appuser:appuser /tmp && \
    chmod 777 /tmp

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8800
USER 1234

CMD ["uvicorn", "convert_server:app", "--host", "0.0.0.0", "--port", "8800"]
