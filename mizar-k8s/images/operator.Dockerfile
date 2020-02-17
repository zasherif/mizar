FROM python:3.7
RUN pip install kopf
RUN pip install kubernetes
RUN pip install pyyaml
COPY operator/ /mizar/operator
CMD kopf run --standalone /mizar/operator/app.py