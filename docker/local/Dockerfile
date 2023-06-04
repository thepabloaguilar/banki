FROM python:3.10

WORKDIR app

COPY ../.. .

COPY docker/local/entrypoint.sh entrypoint.sh

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python - && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
