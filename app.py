from server_llm import *
from fastapi import FastAPI, HTTPException, Request
import uvicorn
from pydantic import BaseModel

app = FastAPI(
    title="Langchain Server", version="1.0", decsription="A simple API Server"
)


# Define data model for the input query
class Query(BaseModel):
    query: str


@app.get("/")
async def hi():
    return {"message": "API is working"}


@app.post("/retrieve/")
async def retrieve_chain(query: Query):
    """Endpoint to interact with the retrieval chain."""
    try:
        # Run the retrieval chain with the input query
        response = retrieval_chain.invoke({"input": query.query})
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
