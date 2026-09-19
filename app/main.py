from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import Agent


app = FastAPI(
    title="Scalable Agentic System",
    description="Agentic system for scalable tool selection and execution",
    version="1.0.0",
)

agent = Agent()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Scalable Agentic System is running",
    }


@app.post("/run")
def run_agent(request: QueryRequest):
    return agent.run(request.query)