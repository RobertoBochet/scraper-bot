FROM python:3.10.0-alpine as compiler

WORKDIR /srv

COPY setup.py ./
COPY README ./
COPY bot_scraper ./bot_scraper

RUN python3 setup.py sdist bdist_wheel

FROM python:3.10.0-alpine

VOLUME /srv

COPY --from=compiler /srv/dist/*.whl /

RUN pip3 install *.whl

ENTRYPOINT python3 -m bot_scraper
