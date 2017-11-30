"""
Server for sending metrics via TCP with specified text protocol
"""
 
import asyncio


class ClientServerProtocol(asyncio.Protocol):
    # metric_database example = {
    # "palm.cpu": {1501864247: 10.5, 1501864248: 0.5, 1501864240: 4.0},
    # "eardrum.cpu": {1501864259: 15.3}, }

    metric_database = {} 
    
    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info("peername")
        print(f"##Connection made: {peername}")

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())
        self.transport.close()              # 'Close the client socket'
    
    @classmethod
    def process_data(cls, data):
        def get_one_metric(what_metric):
            resp = []
            for k,v in cls.metric_database[what_metric].items():
                record = " ".join([what_metric, str(v), str(k), "\n"])
                resp.append(record)
            resp = "".join(resp)
            return resp
            
        what_do = data[0:3]       # "get" / "put"
        what_metric = data[4:-1]  # "palm.cpu" / "eardrum.cpu"
        
        if not data[-1] == "\n":
            return "error\nwrong command\n\n"
            
        if what_do == "get" and data[4] != "*":
            if what_metric in cls.metric_database:
                resp = get_one_metric(what_metric)
                resp = "".join(["ok\n", resp, "\n"])
                return resp
            else:
                return "ok\n\n"
                
        elif what_do == "get" and data[4] == "*" and len(data) == 6:         
            if not cls.metric_database:
                return "ok\n\n"
            resp = []
            for k in cls.metric_database:
                resp.append(get_one_metric(k))
            resp = "".join(resp)
            resp = "".join(["ok\n", resp, "\n"])
            return resp
            
        elif what_do == "put":
            try:
                ls = what_metric.split()
                metric_name = ls[0]
                metric_value = float(ls[1])
                timestamp = int(ls[2]) 
            except Exception as e:
                print(e.__class__, "was occurred with description \n", e )
                return "error\nwrong command\n\n"
            if metric_name not in cls.metric_database:
                cls.metric_database[metric_name] = {}
            cls.metric_database[metric_name][timestamp] = metric_value
            return "ok\n\n"
        else:
            return "error\nwrong command\n\n"

async def wakeup(timer):
    # Added because KeyboardInterrupt don't work properly on Windows
    while True:
        await asyncio.sleep(timer)
            

def main(host, port):
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(ClientServerProtocol, host, port)
    tasks = asyncio.gather(coro, wakeup(3))
    
    try:
        print("TCP-server started.")
        loop.run_until_complete(tasks)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, stopping server...")
    finally:
        tasks.cancel()
        loop.close()
        print("Server stopped")


if __name__ == "__main__":
    host = "localhost"
    port = 8888
    main(host, port)
