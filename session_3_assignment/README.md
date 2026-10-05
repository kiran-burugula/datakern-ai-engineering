# Financial Advisor

## 1. Project Overview

Briefly explain:

- what the service does
- who the client is
- what POST /chat accepts
- that the answer combines portfolio, policy, and current stock news

## 2. Architecture

```text
Client
  |
  v
FastAPI POST /chat
  |
  v
Context Service
  |
  +--> PostgreSQL
  |
  +--> Policy PDF
  |
  +--> Current Stock News
  |
  v
Context Package
  |
  v
Groq LLM
  |
  v
Response
  |
  +--> Phoenix trace
```
