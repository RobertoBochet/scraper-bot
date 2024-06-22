FROM python:3.12-bookworm as compiler

RUN apt update \
    && apt install --no-install-recommends -y \
        curl \
        build-essential \
        pipx

ENV PATH="/root/.local/bin:${PATH}"

RUN pipx install poetry==1.8.3

WORKDIR /app

COPY . .

RUN poetry build --format wheel


FROM python:3.12-alpine

VOLUME /app

COPY --from=compiler /app/dist/*.whl /

RUN pip3 install --no-cache-dir -- *.whl

ENTRYPOINT python3 -m scraper_bot
