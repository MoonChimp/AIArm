#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NEXUS AI - UE5 API Bridge (Simplified)
Basic FastAPI server for UE5 communication
"""

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Pydantic model for request
class ChatRequest(BaseModel):
    message: str

# Create FastAPI app
app = FastAPI(title="Nexus AI UE5 API Simplified")

@app.get("/")
async def root():
    return {"message": "Nexus AI UE5 API Server is running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message
    # Simple response processing
    response = f"AI Processed: '{message}'"
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
