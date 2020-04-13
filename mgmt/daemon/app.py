
import logging
import sys
import os
import proto.droplet_pb2 as droplet_pb2
import proto.droplet_pb2_grpc as droplet_pb2_grpc

from common.common import host_nsenter
from daemon.droplet_service import DropletServer

from concurrent import futures
from google.protobuf import empty_pb2
import time
import grpc

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    droplet_pb2_grpc.add_DropletServiceServicer_to_server(
        DropletServer(), server
    )

    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("server is running")
    try:
        while True:
            time.sleep(100000)
    except KeyboardInterrupt:
        server.stop(0)

