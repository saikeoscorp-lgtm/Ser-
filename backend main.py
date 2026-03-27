from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

relay_state = {
    "desired_state": "off",
    "actual_state": "off",
    "online": False,
    "version": 0
}

class SetRelayRequest(BaseModel):
    state: str

class DeviceStatusRequest(BaseModel):
    actual_state: str

@app.get("/")
def root():
    return {"ok": True, "message": "Relay backend is running"}

@app.get("/api/device/command")
def get_device_command():
    return {
        "desired_state": relay_state["desired_state"],
        "version": relay_state["version"]
    }

@app.post("/api/device/status")
def post_device_status(payload: DeviceStatusRequest):
    relay_state["actual_state"] = payload.actual_state
    relay_state["online"] = True
    return {"ok": True}

@app.get("/api/relay/state")
def get_relay_state():
    return relay_state

@app.post("/api/relay/set")
def set_relay(payload: SetRelayRequest):
    if payload.state not in ["on", "off"]:
        return {"ok": False}

    relay_state["desired_state"] = payload.state
    relay_state["version"] += 1

    return {"ok": True, "relay": relay_state}