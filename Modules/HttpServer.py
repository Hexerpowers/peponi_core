from threading import Thread

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


class HttpServer:
    def __init__(self, config, st, lg):
        self.config = config
        self.st = st
        self.lg = lg

        self.api = FastAPI()
        origins = ["*"]
        self.api.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.server_loop = Thread(target=self.serve, daemon=True, args=())

    def start(self):
        self.server_loop.start()

    def serve(self):
        @self.api.get("/api/v1/trig/manual")
        async def trig_manual():
            self.st.toggle_manual()
            return {
                "status": "OK"
            }

        @self.api.get("/api/v1/trig/record")
        async def trig_record():
            self.st.toggle_record()
            if self.st.get_record():
                result = "on"
            else:
                result = "off"
            return {
                "status": "OK",
                "result": result
            }

        @self.api.get("/api/v1/get/status")
        async def get_status():
            return {
                "status": "OK"
            }

        @self.api.get("/api/v1/get/power")
        async def get_power():
            return {
                "status": "OK",
                "state": self.st.get_power()['state'],
                "voltage": self.st.get_power()['voltage'],
                "current_0": self.st.get_power()['current_0'],
                "current_1": self.st.get_power()['current_1'],
            }

        @self.api.get("/api/v1/get/hank")
        async def get_hank():
            return {
                "state": self.st.get_hank()['state'],
                "direction": self.st.get_hank()['direction'],
                "load": self.st.get_hank()['load'],
                "length": self.st.get_hank()['length'],
                "op_time": self.st.get_hank()['op_time']
            }

        @self.api.post("/api/v1/post/settings")
        async def post_path(data: Request):
            datum = await data.json()
            self.st.set_path(datum['camera_path'])
            self.st.set_endpoint_addr(datum['endpoint_address'])
            self.st.set_hank_params({
                "pull_force": datum['pull_force'],
                "free_length": datum['free_length'],
            })

            return {
                "status": "OK"
            }

        self.lg.log("Принимаю запросы...")
        uvicorn.run(self.api, host="0.0.0.0", port=5053, log_level="critical")
