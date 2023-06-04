import typing as tp

from loguru import logger
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.api.middlewares.auth_backend import parse_token
from app.core.ioc import container, user_services
from app.exceptions.api import ApiError
from app.utils.OtherUtils import generate_code, generate_expired_in
from user.dto import (
    UserLoginDTO,
    UserLogoutDTO,
    UserRefreshTokenDTO,
    UserRegisterDTO,
    UserRequestCodeDTO,
    UserRequestResetPasswordDTO,
    UserResetPasswordDTO,
)

IAuthService = user_services.IAuthService
IUserService = user_services.IUserService


class Registration(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)

    async def post(self, request: Request):
        reg_data = UserRegisterDTO(**dict(await request.json()))
        access_token, refresh_token = await self.__auth_service.register(reg_data)
        output = {"access_token": access_token, "refresh_token": refresh_token}
        await self.__auth_service.send_verification_code(
            UserRequestCodeDTO(
                code=generate_code(),
                email=reg_data.email,
                timestamp=generate_expired_in(),
                reason="complete-register",
            )
        )
        response = JSONResponse(status_code=201, content=output)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="none",
            secure=True,
            max_age=3600 * 24 * 90,  # 90 дней
        )
        response.set_cookie(
            key="status",
            value="not_verified",
            httponly=True,
            samesite="none",
            secure=True,
        )

        logger.info(
            f"user email={reg_data.email} ip={request.client.host} was register"
        )

        return response


class RequestCode(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)

    @requires(scopes="authenticated", status_code=401)
    async def post(self, request: Request):
        await self.__auth_service.request_code(
            request.user.instance.email, "complete-register"
        )
        return Response(status_code=204)


class RedeemCode(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)
    __user_service: IUserService = container.resolve(IUserService)

    @requires(scopes="authenticated", status_code=401)
    async def put(self, request: Request):
        work = await self.__auth_service.redeem_code(
            UserRequestCodeDTO(
                email=request.user.instance.email, **dict(await request.json())
            )
        )
        user = await self.__user_service.find_user_by_id(request.user.instance.id)
        if work is None:
            response = Response(status_code=204)
        else:
            response = JSONResponse(status_code=200, content={"token": work})
        response.set_cookie(
            key="status",
            value=user.status,
            httponly=True,
            samesite="none",
            secure=True,
        )
        return response


class Login(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)

    async def post(self, request: Request):
        data = UserLoginDTO(**dict(await request.json()))
        access_token, refresh_token, user_status = await self.__auth_service.login(data)
        output = {"access_token": access_token, "refresh_token": refresh_token}
        response = JSONResponse(status_code=200, content=output)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="none",
            secure=True,
            max_age=3600 * 24 * 90,  # 90 дней
        )
        response.set_cookie(
            key="status",
            value=user_status,
            httponly=True,
            samesite="none",
            secure=True,
        )

        logger.info(f"user email={data.email} ip={request.client.host} was login")
        return response


class TokenRefresh(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)
    __user_service: IUserService = container.resolve(IUserService)

    async def put(self, request: Request):
        access_token, refresh_token = await self.__auth_service.refresh_token(
            UserRefreshTokenDTO(
                access_token=parse_token(request, "old_access"),
                refresh_token=get_refresh_token_from_cookie(request),
            ),
        )
        payload = await self.__auth_service.decode_access_token(access_token)
        user = await self.__user_service.find_user_by_id(payload["id"])
        output = {"access_token": access_token, "refresh_token": refresh_token}
        response = JSONResponse(status_code=200, content=output)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="none",
            secure=True,
            max_age=3600 * 24 * 90,  # 90 дней
        )
        response.set_cookie(
            key="status",
            value=user.status,
            httponly=True,
            samesite="none",
            secure=True,
        )
        return response


class Logout(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)

    @requires(scopes="authenticated", status_code=401)
    async def delete(self, request: Request):
        await self.__auth_service.logout(
            UserLogoutDTO(
                user=request.user.instance,
                refresh_token=get_refresh_token_from_cookie(request),
            )
        )
        response = Response(status_code=204)
        response.delete_cookie("refresh_token")
        response.delete_cookie("status")
        return response


class LogoutEverywhere(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)

    @requires(scopes="authenticated", status_code=401)
    async def delete(self, request: Request):
        await self.__auth_service.logout_everywhere(request.user.instance)
        response = Response(status_code=204)
        response.delete_cookie("refresh_token")
        response.delete_cookie("status")
        return response


class ResetPassword(HTTPEndpoint):
    __auth_service: IAuthService = container.resolve(IAuthService)
    __user_service: IUserService = container.resolve(IUserService)

    async def post(self, request: Request):
        data = UserRequestResetPasswordDTO(**await request.json())
        dto = UserRequestCodeDTO(
            code=generate_code(),
            reason="reset-password",
            email=data.email,
            timestamp=generate_expired_in(),
        )
        await self.__auth_service.request_reset_password(dto)

        logger.info(
            f"user email={data.email} ip={request.client.host} send reset password request"
        )

        return Response(status_code=204)

    async def patch(self, request: Request):
        work = await self.__auth_service.redeem_code(
            UserRequestCodeDTO(**dict(await request.json()))
        )

        return JSONResponse(status_code=200, content={"token": work})

    async def put(self, request: Request):
        data = await request.json()
        dto = UserResetPasswordDTO(token=request.query_params["token"], **data)
        email = await self.__auth_service.reset_password(dto)

        access_token, refresh_token, user_status = await self.__auth_service.login(
            UserLoginDTO(email=email, password=data["password"])
        )
        output = {"access_token": access_token, "refresh_token": refresh_token}
        response = JSONResponse(status_code=200, content=output)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="none",
            secure=True,
            max_age=3600 * 24 * 90,  # 90 дней
        )
        response.set_cookie(
            key="status",
            value=user_status,
            httponly=True,
            samesite="none",
            secure=True,
        )

        logger.info(
            f"user email={email} ip={request.client.host} send changed password"
        )

        return response


def get_refresh_token_from_cookie(request: Request):
    token = request.cookies.get("refresh_token", None)
    if token is None:
        raise ApiError.forbidden(message="Refresh token not found")
    return token
