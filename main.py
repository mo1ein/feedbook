import uvicorn
from src.logics.auth import AuthLogic
from src.models.auth_model import VerifyAccessTokenInputModel
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.requests import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.services.private_routes import routes

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
        print(credentials.credentials)
        response = auth_logic.verify_access_token(input_model)
    except Exception as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication Credentials",
        ) from exception
    if customer_uuid := request.path_params.get('customer_uuid'):
        if customer_uuid != str(response.customer_uuid):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="DO NOT HAVE ENOUGH PRIVILEGES TO PERFORM AN ACTION ON A RESOURCE",
            )


def _add_routes(app):
    dependencies = [
        Depends(validate_customer_authentication),
        # TODO: rate limit
    ]
    responses = base_responses | {
        401: {"description": "Invalid Authentication Credentials"},
        403: {"description": "HAVE NOT ENOUGH PRIVILEGES TO PERFORM AN ACTION OR ACCESS A RESOURCE"},
    }
    app.include_router(routes, dependencies=dependencies, responses=responses)


def _create_app():
    app = FastAPI()
    _add_routes(app)
    return app

def serve():
    app = _create_app()
    # add uvicorn configs...
    uvicorn.run(app,port=9000)

if __name__ == '__main__':
    from src.utils.configs import Configuration
    # fix dotenv...
    # Configuration.apply(RuntimeConfig, alternative_env_search_dir=__file__)
    serve()
