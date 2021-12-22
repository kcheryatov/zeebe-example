import json
import time

import grpc
from zeebe_grpc import gateway_pb2, gateway_pb2_grpc

with grpc.insecure_channel("192.1.1.5:26500") as channel:
    stub = gateway_pb2_grpc.GatewayStub(channel)

    # print the topology of the zeebe cluster
    topology = stub.Topology(gateway_pb2.TopologyRequest())
    print(topology)

    # start a process instance
    for i in range(200):
        variables = {
            "orderId": 8000+i
        }
        res = stub.CreateProcessInstance(
            gateway_pb2.CreateProcessInstanceRequest(
                bpmnProcessId="order_process_2",
                version=-1,
                variables=json.dumps(variables)
            )
        )
        print(res)
        time.sleep(0.01)

