import typing as tp

from starlette.requests import Request
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse, JSONResponse
from user.dto.user import UserRegisterDTO, UserVerificationData
from app.core.ioc import container, user_services
from app.utils.OtherUtils import generate_code, generate_expired_in

IUserService = user_services.IUserService


class Registration(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    async def post(self, request: Request):
        reg_data = UserRegisterDTO(**dict(await request.json()))
        result = await self.__service.create_user(reg_data)
        await self.__service.send_verification_code(UserVerificationData(
            ip=request.client.host,
            id=result.id,
            code=generate_code(),
            email=result.email,
            timestamp=generate_expired_in()
        ))
        return JSONResponse(
            status_code=201,
            content=result.dict()
        )


#TODO: добавить тип запроса (с какой целью нужен код). При вводе кода, проверять этот тип
class RequestCode(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    async def put(self, request: Request):
        body = dict(await request.json())
        await self.__service.request_code(body.get('email'), request.client.host)
        return PlainTextResponse()


class RegistrationComplete(HTTPEndpoint):
    __service: IUserService = container.resolve(IUserService)

    async def put(self, request: Request):
        user = await self.__service.complete_register(
            UserVerificationData(ip=request.client.host, **dict(await request.json())))
        return JSONResponse(
            status_code=200,
            content=user.dict()
        )


class Login(HTTPEndpoint):
    async def post(self, request: Request):
        ...


class TokenRefresh(HTTPEndpoint):
    async def put(self, request: Request):
        ...


class Logout(HTTPEndpoint):
    async def delete(self, request: Request):
        ...
