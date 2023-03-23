from threading import Thread

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


class Dimensions(BaseModel):
    field_width: str
    field_height: str


class Telemetry(BaseModel):
    charge_level: str
    signal_strength: str


class Transport:
    def __init__(self, config, st, lg):
        self.config = config
        self.st = st
        self.lg = lg

        self.api = FastAPI()
        self.server_loop = Thread(target=self.serve, daemon=True, args=())

    def start(self):
        self.server_loop.start()

    def serve(self):
        @self.api.get("/api/v1/status")
        async def status_get():
            return {"status": "OK"}

        @self.api.get("/api/v1/get_position")
        async def position_get():
            return {
                "status": "OK",
                "position": self.st.get_position(),
            }

        @self.api.get("/api/v1/get_telemetry")
        async def telemetry_get():
            return {
                "status": "OK",
                "telemetry": self.st.get_telemetry(),
            }

        @self.api.post("/api/v1/set_dimens")
        async def dimens_set(dimensions: Dimensions):
            self.st.set_dimens(
                field_width=dimensions.field_width,
                field_height=dimensions.field_height,
                offset_x=0,
                offset_y=0.45,
                magic_x=5000,
                magic_y=3637
            )
            return {
                "status": "OK",
                "dimensions": self.st.get_params(),
            }

        @self.api.post("/api/v1/set_telemetry")
        async def telemetry_set(telemetry: Telemetry):
            self.st.set_telemetry(
                charge_level=telemetry.charge_level,
                signal_strength=telemetry.signal_strength
            )
            return {
                "status": "OK",
                "dimensions": self.st.get_telemetry(),
            }

        uvicorn.run(self.api, host="0.0.0.0", port=8000)
