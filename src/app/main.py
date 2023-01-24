from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.context import get_context
from app.middleware.redis_session import RedisSessionMiddleware
from app.resources.members.endpoints import router as members_router


# -----------------------------------------------------------------------------
# Instance of FastAPI Application
# -----------------------------------------------------------------------------
app = FastAPI(
    title="DarkStar REST API",
    description="More description will be added soon",
    version="1.0.0",
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
# during authorization
app.add_middleware(
    RedisSessionMiddleware,
    signing_key=get_context().middleware_key,
    cookie_name='darkstar',
    redis=get_context().redis_connection
)


# Members Router Inclusion
app.include_router(members_router, prefix=f"/api/{get_context().api_version}")
