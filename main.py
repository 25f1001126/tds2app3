from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API_KEY = "ak_4qfai9ezz4ng84f0o66qbdta"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class Payload(BaseModel):
    events: list[Event]


@app.post("/analytics")
def analytics(
    payload: Payload,
    x_api_key: str | None = Header(default=None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    totals = {}
    revenue = 0.0

    for event in payload.events:
        if event.amount > 0:
            revenue += event.amount
            totals[event.user] = totals.get(event.user, 0) + event.amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": "25f1001126@ds.study.iitm.ac.in",
        "total_events": len(payload.events),
        "unique_users": len({e.user for e in payload.events}),
        "revenue": revenue,
        "top_user": top_user,
    }
