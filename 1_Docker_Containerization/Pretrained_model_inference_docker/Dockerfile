FROM python:3.9-slim-buster as compile-image

RUN apt-get update -y && apt install -y --no-install-recommends git\
    && pip install --no-cache-dir -U pip

COPY requirements.txt .

RUN pip install --user --no-cache-dir https://download.pytorch.org/whl/cpu/torch-1.11.0%2Bcpu-cp39-cp39-linux_x86_64.whl \
    && pip install --user --no-cache-dir https://download.pytorch.org/whl/cpu/torchvision-0.12.0%2Bcpu-cp39-cp39-linux_x86_64.whl \
    && pip install --user --no-cache-dir -r requirements.txt && rm -rf /root/.cache/pip

FROM python:3.9-slim-buster as runtime-image
COPY --from=compile-image /root/.local /root/.local
WORKDIR /src
COPY . .
ENTRYPOINT ["python3", "app.py"]
