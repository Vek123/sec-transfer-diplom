FROM alpine/openssl:latest AS certs

WORKDIR /certs/

RUN openssl ecparam -genkey -name secp384r1 -out key.pem
RUN openssl req -x509 -new -key key.pem -out cert.pem -days 3650 -subj "/C=RU/ST=MOSCOW/CN='Security Transfer'"


FROM python:3.11-alpine

WORKDIR /sec_transfer/

RUN apk update
RUN apk upgrade
RUN apk add gettext

COPY ./.python-version ./
RUN python3 -m venv .venv
RUN source .venv/bin/activate

COPY ./requirements ./requirements
RUN pip3 install -r requirements/prod.txt

COPY ./sec_transfer/ ./sec_transfer/

ENV DJANGO_DEBUG=False
RUN python3 ./sec_transfer/manage.py compilemessages

COPY --from=certs /certs/ ./certs/

WORKDIR /sec_transfer/sec_transfer/

CMD ["sh", "-c", "python3 manage.py migrate && gunicorn --keyfile /sec_transfer/certs/key.pem --certfile /sec_transfer/certs/cert.pem --ssl-version TLS_SERVER -w $(nproc) -b 0.0.0.0:80 sec_transfer.wsgi:application"]
