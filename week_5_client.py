"""
Client for sending metrics via TCP text
"""
 

import socket
import time

# servers "palm", "eardrum",
# metrics "cpu", "memory usage", "disk usage", "network usage",


class ClientError(OSError):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = str(host)
        self.port = int(port)
        self.timeout = float(timeout)
    
    @staticmethod
    def parse_server_response(resp, who_call=None):
        if who_call == "put":
            if resp == "ok\n\n":
                return True, "Metric has sent successfully"
            elif resp == "error\nwrong command\n\n":
                return False, "Server response: wrong command"
            else:
                return False, "Server hasn't confirmed receiving data"
        elif who_call == "get":
            if resp == "ok\n\n":
                return True, {}
            elif resp[0:2] == "ok" and resp[-2:] == "\n\n":
                metric_dict = {}
                resp = resp.split("\n")[1:-2]
                for metric in resp:
                    metric = metric.split()
                    if metric[0] in metric_dict:
                        metric_dict[metric[0]].append((int(metric[2]), float(metric[1])))
                    else:
                        metric_dict[metric[0]] = [(int(metric[2]), float(metric[1]))]
                for key in metric_dict:
                    metric_dict[key].sort()
                return True, metric_dict
            else:
                return False, "Server's response is not described"

    def handle_connect(self, message, who_call=None):
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            try:
                sock.sendall(message.encode("utf-8"))
                response = sock.recv(4096)
                resp = Client.parse_server_response(response.decode("utf-8"), who_call)
                return resp
            except socket.timeout:
                return False, "Client send data timeout"
            except socket.error:
                return False, "Client send data error"

    def put(self, server_dot_metric, metric_value, timestamp=None):
        if not timestamp:
            timestamp = int(time.time())
        message = f"put {server_dot_metric} {metric_value} {timestamp}\n"
        resp = self.handle_connect(message, who_call="put")
        if not resp[0]:
            print(resp[1])
            raise ClientError
        else:
            print(resp[1])

    def get(self, metric):
        message = f"get {metric}\n"
        resp = self.handle_connect(message, who_call="get")
        if resp[0]:
            return resp[1]
        else:
            print(resp[1])
            raise ClientError


def main(host, port, timeout):
    client = Client(host, port, timeout)
    client.put("palm.cpu", 0.5, timestamp=1150864247)
    client.put("palm.cpu", 2.0, timestamp=1150864248)
    client.put("palm.cpu", 0.5, timestamp=1150864248)
    client.put("eardrum.cpu", 3, timestamp=1150864250)
    client.put("eardrum.cpu", 4, timestamp=1150864251)
    client.put("eardrum.memory", 4200000)
    print(client.get("palm.cpu"))
    print(client.get("eardrum.memory"))
    print(client.get("*"))
    for i in range(0,10):
        time.sleep(1)
        print(client.get("eardrum.memory"))
    print("Client session is closed")
    

if __name__ == "__main__":
    host = "localhost"
    port = 8888
    timeout = 5
    main(host, port, timeout)
