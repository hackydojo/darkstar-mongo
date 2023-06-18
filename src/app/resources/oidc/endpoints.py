from fastapi import APIRouter
from starlette.requests import Request

from app.security.oidc import get_oauth

router = APIRouter()


# ---------------------------------------------------------
# METHOD AUTHORIZE THROUGH OIDC
# ---------------------------------------------------------
@router.get("/oidc/authorize")
async def authorize_through_oidc(request: Request):
    redirect_uri = request.url_for("oidc_callback").replace("http://", "https://")
    oauth = get_oauth()
    return await oauth.oidc_provider.authorize_redirect(request, redirect_uri)


# ---------------------------------------------------------
# METHOD OIDC CALLBACK
# ---------------------------------------------------------
@router.get("/oidc/authorize")
async def oidc_callback(request: Request):
    """
    TODO implement OIDC callback
    :param request:
    :return:
    """
    pass
