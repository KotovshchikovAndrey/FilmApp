import typing as tp

from starlette.requests import Request
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse, JSONResponse

from user.dto import UserRefreshTokenDTO
from user.dto.user import UserRegisterDTO, UserVerificationData, UserLoginDTO
from app.core.ioc import container, user_services
from app.utils.OtherUtils import generate_code, generate_expired_in

IAuthService = user_services.IAuthService


class Registration(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)

    async def post(self, request: Request):
        reg_data = UserRegisterDTO(**dict(await request.json()))
        access_token, refresh_token = await self.__auth_service.register(reg_data)
        output = {"access_token": access_token, "refresh_token": refresh_token}
        await self.__auth_service.send_verification_code(UserVerificationData(
            ip=request.client.host,
            code=generate_code(),
            email=reg_data.email,
            timestamp=generate_expired_in(),
            reason="complete-register"
        ))
        response = JSONResponse(
            status_code=201,
            content=output
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=3600 * 24 * 90,  # 90 дней
        )
        return response


class RequestCode(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)

    @requires("authenticated")
    async def put(self, request: Request):
        body = dict(await request.json())
        await self.__auth_service.request_code(body.get('email'), request.client.host, body.get('reason'))
        return PlainTextResponse()


class RegistrationComplete(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)

    @requires("authenticated")
    async def put(self, request: Request):
        user = await self.__auth_service.complete_register(
            UserVerificationData(ip=request.client.host, reason="complete-register", **dict(await request.json())))
        return JSONResponse(
            status_code=200,
            content=user.dict()
        )


class Login(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)

    async def post(self, request: Request):
        data = UserLoginDTO(**dict(await request.json()))
        access_token, refresh_token = await self.__auth_service.login(data)
        output = {"access_token": access_token, "refresh_token": refresh_token}
        response = JSONResponse(
            status_code=200,
            content=output
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=3600 * 24 * 90,  # 90 дней
        )
        return response


class TokenRefresh(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)

    @requires("authenticated")
    async def put(self, request: Request):
        access_token, refresh_token = await self.__auth_service.refresh_token(
            UserRefreshTokenDTO(
                user=request.user.instance,
                **dict(await request.json()),
            ),
        )
        output = {"access_token": access_token, "refresh_token": refresh_token}
        response = JSONResponse(
            status_code=200,
            content=output
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=3600 * 24 * 90,  # 90 дней
        )
        return response


class Logout(HTTPEndpoint):
    @requires("authenticated")
    async def delete(self, request: Request):
        ...


class LogoutEverywhere(HTTPEndpoint):
    @requires("authenticated")
    async def delete(self, request: Request):
        ...
