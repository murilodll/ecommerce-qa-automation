FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
        | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" \
        > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        nodejs \
        python3 \
        python3-venv \
        openjdk-21-jdk-headless \
        maven \
    && apt-get purge -y --auto-remove curl gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --no-audit --no-fund \
    && npm cache clean --force

RUN npx playwright install --with-deps --only-shell chromium

COPY config/requirements.txt /tmp/requirements.txt

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-compile -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

EXPOSE 8501 8502

CMD ["python", "-m", "streamlit", "run", "src/main.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]