from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.context import get_context
from app.endpoints import benchmark, vulnerability


# -----------------------------------------------------------------------------
# Instance of FastAPI Application
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Vulnerability Automation Platform - Heimdall API",
    description="Heimdall is a Vulnerability "
    "Management Platform designed to be"
    "highly scalable, flexible and "
    "capable of managing and tracking "
    "vulnerabilities in real time ",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/",
    redoc_url=None,
)

# -----------------------------------------------------------------------------
# CORS RULES
# -----------------------------------------------------------------------------
origins = ["*"]

# Default configuration is to ALLOW ALL from EVERYWHERE. You might want to
# restrict this.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is required to temporary save code and state in the session
# during authorization with w3id
app.add_middleware(SessionMiddleware, secret_key=get_context().middleware_key)

app.include_router(
    benchmark.router, prefix=f"/api/{get_context().as_str('API_VERSION')}"
)
app.include_router(
    vulnerability.router, prefix=f"/api/{get_context().as_str('API_VERSION')}"
)
