from fastapi import HTTPException

from src.logics.auth import AuthLogic
from src.models.auth_model import LoginInputModel, LoginOutputModel, RegisterOutputModel, RegisterInputModel

auth_logic = AuthLogic()


def test_login():
    # login correct way
    login_model = LoginInputModel(email='x@x.com', password='1qaz@WSX')
    output = auth_logic.login(login_model)
    assert isinstance(output, LoginOutputModel)

    # email or password is wrong
    login_model = LoginInputModel(email='akbar@gmail.com', password='9090ak@oOk$')
    try:
        output = auth_logic.login(login_model)
    except HTTPException:
        assert True


def test_register():
    register_model = RegisterInputModel(
        email='azhdar@gmail.com',
        name='azhdar',
        last_name='digikalaeian',
        password='1qaz@WSX'
    )
    output = auth_logic.register(register_model)
    assert isinstance(output, RegisterOutputModel)


def test_verify_access_token():
    ...
