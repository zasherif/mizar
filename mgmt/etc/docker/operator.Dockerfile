# SPDX-License-Identifier: MIT
# Copyright (c) 2020 The Authors.

# Authors: Sherif Abdelwahab <@zasherif>
#          Phu Tran          <@phudtran>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:The above copyright
# notice and this permission notice shall be included in all copies or
# substantial portions of the Software.THE SOFTWARE IS PROVIDED "AS IS",
# WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

FROM python:3.7
RUN pip install kopf
RUN pip install kubernetes
RUN pip install pyyaml
RUN pip install netaddr
RUN pip install ipaddress
RUN pip install rpyc
RUN pip install luigi
RUN pip install protobuf
RUN pip install grpcio-tools
RUN apt-get update -y
RUN apt-get install net-tools
COPY mgmt/ /var/mizar/mgmt/
COPY build/ /var/mizar/mgmt/build
RUN ln -snf /var/mizar/mgmt/build/bin /trn_bin
RUN mkdir -p /var/run/luigi
RUN mkdir -p /var/log/luigi
RUN mkdir -p /var/lib/luigi
RUN mkdir -p /etc/luigi
COPY mgmt/etc/luigi.cfg /etc/luigi/luigi.cfg
CMD kopf run --standalone /var/mizar/mgmt/operator.py