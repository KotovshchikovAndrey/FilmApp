from starlette.routing import Route

from app.api.api_v1.auth import controllers

routes = [
    Route("/register", controllers.Registration),
    Route("/request-code", controllers.RequestCode),
    Route("/redeem-code", controllers.RedeemCode),
    Route("/login", controllers.Login),
    Route("/refresh-token", controllers.TokenRefresh),
    Route("/logout", controllers.Logout),
    Route("/logout-everywhere", controllers.LogoutEverywhere),
]
