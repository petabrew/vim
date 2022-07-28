import socket
import time
import threading
import json

DEBUG = False

'''
{"data" : [
        {
            "module_id": 111,
            "elb_data": [
                {"status": 1, "current": 20, "voltage" 220},
            ]
        }, 
        {
            "module_id": 222,
            "elb_data": [
                {"status": 1, "current": 20, "voltage" 220},
                {"status": 1, "current": 20, "voltage" 220},
                {"status": 1, "current": 20, "voltage" 220},
                {"status": 1, "current": 20, "voltage" 220},
                {"status": 1, "current": 20, "voltage" 220},
                {"status": 1, "current": 20, "voltage" 220},
                {"status": 1, "current": 20, "voltage" 220}
            ] // elb_list
        } // module dict
    ] // Data List
}
server_packet_data = {
    2: {
            'module_id': 2, 
            'elb_data': [{'status': 2, 'current': 0, 'voltage': 250}], 
            'timestamp': 1646674067, 
            'timedelta': 5,
            'count': 20
        }, 
    1: {
            'module_id': 1, 
            'elb_data': [{'status': 2, 'current': 0, 'voltage': 250}], 
            'timestamp': 1646674072, 
            'timedelta': 0
        }
}
'''

class UdpTask:
    def __init__(self):
        self.count = 0
        self.addr = 0
        self.ready = False
        self.module_data = {}
        self.module_addr = {}
        self.module_count = {}
        self.conn()

    def conn(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.ready = True

        except:
            self.ready = False

    def udp_task(self):
        self.sock.bind(("0.0.0.0", 63503))
        while True:
            try:
                time.sleep(0.1)
                new_module_data = {}
                msg, addr = self.sock.recvfrom(4096)

                if msg:
                    t_now = int(time.time())
                    self.count += 1
                    msg2 = json.loads(msg.decode())
                    data_list = msg2.get("data") # list
                    for module in data_list: 
                        m = module.get("module_id")
                        if m:
                            module_id = int(m)
                            if self.module_data.get(module_id): 
                                count = self.module_data[module_id].get("count")
                            else:
                                count = 0

                            new_module_data = {
                                "module_id": module_id,
                                "elb_data": module.get("elb_data"),
                                "timestamp": t_now,
                                "timedelta": t_now,
                                "count": count + 1
                            }
                            # Data update
                            self.module_data[module_id] = new_module_data
                            # Update addr
                            self.module_addr[module_id] = addr
                    # end For

                    # Update timedelta
                    for i in self.module_data:
                        timedelta = t_now - self.module_data[i].get("timestamp")
                        if timedelta < 30:
                            self.module_data[i]["timedelta"] = timedelta
                        else:
                            for j in self.module_data[i]["elb_data"]:
                                j["status"] = 0

                            # Update timedelta
                            for i in self.module_data:
                                self.module_data[i]["timedelta"] = t_now - self.module_data[i].get("timestamp")
                            # Update addr
                            self.module_addr[module_id] = addr

                    if DEBUG:
                        for i in self.module_data:
                            print(i, self.module_data[i], self.module_addr[i])

            except Exception as e:
                print(e)
                pass


    def send_elb_msg(self, onoff, module_id, elb_id):
        try:
            msg = {
                "onoff": onoff,
                "module_id": module_id,
                "elb_id": elb_id,
            }
            addr = self.module_addr.get(module_id)
            time.sleep(0.1)
            if addr:
                self.sock.sendto(json.dumps(msg).encode(), addr)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def get_count(self, module_id):
        return self.module_count.get(module_id)

    def loop(self):
        threading.Thread(target=self.udp_task).start()

if __name__ == "__main__":
    udp_task = UdpTask()
    udp_task.loop()

