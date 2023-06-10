from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from app.core import config
from app.api.api_v1.user import controllers

routes = [
    Route("/profile/{user_id:int}", controllers.Profile),
    Route("/favorite/{user_id:int}", controllers.UserFavorite),
    Route("/watch-status", controllers.MyWatchStatus),
    Route("/profile/me", controllers.MyProfile),
    Route("/profile/me/toggle-visibility", controllers.MyProfileVisibility),
    Route("/profile/{user_id:int}/toggle-visibility", controllers.ProfileVisibility),
    Route("/profile/me/avatar", controllers.ProfileAvatar),
    Route("/favorite/me", controllers.MyFavorite),
    Route("/{user_id:int}/ban", controllers.BanUser),
    Route("/{user_id:int}/unban", controllers.UnbanUser),
    Route("/change-password", controllers.ChangePassword),
    Route("/change-email", controllers.ChangeEmail),
    Mount(
        "/media",
        app=StaticFiles(directory=config.UPLOAD_DIR + "/avatars"),
        name="static",
    ),
]
