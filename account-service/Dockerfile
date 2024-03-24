FROM sanicframework/sanic:3.10-latest

WORKDIR /sanic

RUN apk add --no-cache \
        curl \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev

RUN pip install poetry

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-cache --no-dev

COPY . .

CMD ["poetry", "run", "python", "server.py"]

EXPOSE 8000