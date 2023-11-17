import uvicorn
from src.logics.auth import AuthLogic
from src.models.auth_model import VerifyAccessTokenInputModel
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.requests import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.services.private_services import private_routes
from src.services.public_services import public_routes

app = FastAPI()
bearer_scheme = HTTPBearer()

base_responses = {
    400: {"description": "Invalid Input Arguments"},
    504: {"description": "Request Process Timed Out"},
    404: {"description": "Requested Resource Not Found"},
    409: {"description": "Requested Entity Already Exists or Faced a conflict"},
    429: {"description": "Too Many Requests Sent"},
    503: {"description": "Service Temporary Unavailable"},
    501: {"description": "Requested Method Not Implemented"},
    500: {"description": "Internal Server Error"},
}


def validate_customer_authentication(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    auth_logic = AuthLogic()
    try:
        input_model = VerifyAccessTokenInputModel(access_token=credentials.credentials)
        response = auth_logic.verify_access_token(input_model)
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication Credentials",
        ) from exception
    if user_id := request.path_params.get('usesr_id'):
        if user_id != str(response.user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="DO NOT HAVE ENOUGH PRIVILEGES TO PERFORM AN ACTION ON A RESOURCE",
            )


def _add_public_routes(app):
    dependencies = [
        # TODO: rate limit
    ]
    responses = base_responses | {
        401: {"description": "Invalid Authentication Credentials"},
        403: {"description": "HAVE NOT ENOUGH PRIVILEGES TO PERFORM AN ACTION OR ACCESS A RESOURCE"},
    }
    app.include_router(public_routes, dependencies=dependencies, responses=responses)


def _add_private_routes(app):
    dependencies = [
        Depends(validate_customer_authentication),
        # TODO: rate limit
    ]
    responses = base_responses | {
        401: {"description": "Invalid Authentication Credentials"},
        403: {"description": "HAVE NOT ENOUGH PRIVILEGES TO PERFORM AN ACTION OR ACCESS A RESOURCE"},
    }
    app.include_router(private_routes, dependencies=dependencies, responses=responses)


def _add_routers(app):
    _add_public_routes(app)
    _add_private_routes(app)


def _create_app():
    app = FastAPI()
    _add_routers(app)
    return app


def serve():
    app = _create_app()
    # add uvicorn configs...
    uvicorn.run(app, port=9000)


if __name__ == '__main__':
    from src.utils.configs import Configuration

    # fix dotenv...
    # Configuration.apply(RuntimeConfig, alternative_env_search_dir=__file__)
    serve()
