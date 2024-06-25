FROM python:3.10 as base

WORKDIR /core

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install --no-install-recommends -y && apt-get install -y git

COPY requirements /requirements
COPY scripts /scripts

RUN python3 -m pip install --upgrade pip && pip install --no-cache-dir -r /requirements/production.txt && rm -rf /var/lib/apt/lists/*


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ multy stage
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /core

COPY --from=base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY --from=base /scripts /scripts
COPY . /core

EXPOSE 8000/tcp
ENV PORT 8000

CMD ["/scripts/start.sh"]
