FROM python:3.5

RUN mkdir /opt/monitor

COPY es_utils.py /opt/monitor
COPY k8spodmonitor1.py /opt/monitor
COPY monitor.py /opt/monitor/
COPY spark_rest.py /opt/monitor
COPY utils.py /opt/monitor
COPY config /opt/monitor
COPY ca /opt/monitor

RUN pip3 install kubernetes

WORKDIR /opt/monitor

CMD  ["python3", "monitor.py"]
