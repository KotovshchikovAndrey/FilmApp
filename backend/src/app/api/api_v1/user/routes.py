from starlette.routing import Route
from app.api.api_v1.user import controllers

routes = [
    Route("/profile/{user_id:int}", controllers.Profile),
    Route("/favorite/{user_id:int}", controllers.UserFavorite),
    Route("/profile/me", controllers.MyProfile),
    Route("/favorite/me", controllers.MyFavorite),
]
