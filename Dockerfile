FROM python:3.10.0-alpine as compiler

WORKDIR /srv

COPY setup.py ./
COPY README ./
COPY scraper_bot ./scraper_bot

RUN python3 setup.py sdist bdist_wheel

FROM python:3.10.0-alpine

VOLUME /srv

COPY --from=compiler /srv/dist/*.whl /

RUN pip3 install *.whl

ENTRYPOINT python3 -m scraper_bot
