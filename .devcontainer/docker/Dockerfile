# Fabric Runtime 1.3: 
FROM spark:4.0.0-scala2.13-java21-ubuntu

USER 0

RUN echo 'python3 -m pytest tests/' >> /root/.bash_history

# Install Python 3.12
RUN set -ex; \
    apt-get update; \
    apt-get install -y software-properties-common; \
    add-apt-repository ppa:deadsnakes/ppa; \
    apt-get update; \
    apt-get install -y python3.12 python3.12-venv python3.12-dev; \
    rm -rf /var/lib/apt/lists/*

# Install pip using get-pip.py
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.12 get-pip.py && rm get-pip.py

# Update alternatives to set Python 3.12 as the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
# Upgrade pip to the latest version
RUN python3 -m pip install --upgrade pip
# Update package list and install Git
RUN apt-get update && apt-get install -y git

# Install uv (Universal Virtualenv) 
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /code
COPY docker/requirements.txt .
COPY docker/stubs-requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


CMD ["tail", "-f", "/dev/null"]