FROM python:3.12-slim

#Set the working directory
WORKDIR /usr/src/app

COPY pyproject.toml .

RUN apt-get update && apt-get install -y wget && apt-get clean && rm -rf /var/cache/apt/
RUN cd /tmp/ && wget https://github.com/pysnmp/mibs/archive/refs/tags/v1.15.8.tar.gz && \
    find /tmp/ -name "v1.15.8.tar.gz" -exec tar -xvf "{}" \; && \
    mkdir -p /usr/share/snmp/mibs/ && \
    find /tmp/ -path '*src/standard/*' -type f -exec cp "{}" /usr/share/snmp/mibs/ \; && \
    rm -rf /tmp/mibs*


#copy all the files
RUN mkdir snmp_json
COPY snmp_json snmp_json/
RUN touch README.md

RUN adduser snmp
USER snmp

RUN python -m pip install .

#Run the command
ENTRYPOINT [ "/home/snmp/.local/bin/snmp-json" ]