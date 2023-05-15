from starlette.routing import Route
from app.api.api_v1.auth import controllers

routes = [
    Route("/register", controllers.Registration),
    Route("/request-code", controllers.RequestCode),
    Route("/register-complete", controllers.RegistrationComplete),
    Route("/login", controllers.Login),
    Route("/refreshToken", controllers.TokenRefresh),
    Route("/logout", controllers.Logout),
]
