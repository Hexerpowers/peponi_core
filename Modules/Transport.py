from threading import Thread

from fastapi import FastAPI, Request
import uvicorn


class Transport:
    def __init__(self, config, st, lg):
        self.config = config
        self.st = st
        self.lg = lg

        self.api = FastAPI()
        self.server_loop = Thread(target=self.serve, daemon=True, args=())

    def start(self):
        self.server_loop.start()

    @staticmethod
    def sanitize(position):
        return {
            "pos_x":0,
            "pos_y":0
        }

    def serve(self):
        @self.api.get("/api/v1/get/status")
        async def get_status():
            return {"status": "OK"}

        @self.api.post("/api/v1/get/position")
        async def get_position(data: Request):
            theta = await data.json()
            self.st.set_theta(theta['theta'])
            return {
                "position": self.st.get_position(0)
            }

        @self.api.get("/api/v1/get/telemetry")
        async def get_telemetry():
            return {
                "telemetry": self.st.get_telemetry(),
            }

        @self.api.get("/api/v1/get/runtime")
        async def get_runtime():
            return {
                "runtime": self.st.get_runtime(),
            }

        @self.api.post("/api/v1/set/position")
        async def set_position(position: Request):
            req_info = await position.json()
            san_position = self.sanitize(req_info)
            self.st.set_position(2, self.st.get_position(1))
            self.st.set_position(1, self.st.get_position(0))
            self.st.set_position(
                san_position['pos_x'],
                san_position['pos_y']
            )
            return {"status": "OK"}

        @self.api.post("/api/v1/set/telemetry")
        async def set_telemetry(telemetry: Request):
            req_info = await telemetry.json()
            self.st.set_telemetry(
                charge_level=req_info['charge_level'],
                signal_strength=req_info['signal_strength']
            )
            return {"status": "OK"}

        @self.api.post("/api/v1/set/route")
        async def set_route(route: Request):
            req_info = await route.json()
            self.st.set_route(req_info['route'])
            return {"status": "OK"}

        self.lg.log("Принимаю запросы...")
        uvicorn.run(self.api, host="0.0.0.0", port=5252, log_level="critical")
