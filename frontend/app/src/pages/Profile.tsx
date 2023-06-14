import * as React from "react"
import { Avatar, Box, Button, CircularProgress, Skeleton, Stack, Typography } from "@mui/material"
import { useAppDispatch, useAppSelector } from "../store"
import { Navigate } from "react-router-dom"
import { fetchUserFavoriteFilms, logoutUser, setUserAvatar } from "../store/actionCreators"
import ArrowHeader from "../components/shared/Header/ArrowHeader"
import ProfileDataField from "../components/shared/Profile/ProfileDataField"
import FilmCardList from "../components/shared/film/FilmCardList"
import { API_URL } from "../core/config"

export default function Profile() {
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const isLoading = useAppSelector((state) => state.auth.loading)
  const user = useAppSelector((state) => state.auth.user)

  const favoriteFilms = useAppSelector((state) => state.film.favoriteFilms)

  React.useEffect(() => {
    dispatch(fetchUserFavoriteFilms())
  }, [])

  const UploadAvatarHandler = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files) {
      const avatar = files[0]
      if (avatar) {
        const formData = new FormData()
        formData.append("avatar", files[0])

        dispatch(setUserAvatar(formData))
      }
    }
  }

  const renderProfile = () => (
    <React.Fragment>
      <ArrowHeader />
      <Stack spacing={3} mt={5} useFlexGap>
        {user !== null && (
          <>
            {isLoading ? (
              <Box display="flex">
                <CircularProgress size={100} />
              </Box>
            ) : (
              <Avatar
                src={
                  user.avatar
                    ? `${API_URL}/users/media` + user.avatar
                    : "https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"
                }
                sx={{ width: 100, height: 100 }}
              />
            )}

            <Typography variant="h3">Welcome {user.name}</Typography>
            <Stack spacing={3} my={5} maxWidth={600} useFlexGap>
              <ProfileDataField userDataName="Name" userDataValue={user.name} />
              <ProfileDataField userDataName="Surname" userDataValue={user.surname} />
              <ProfileDataField userDataName="Email" userDataValue={user.email} />
              <ProfileDataField userDataName="Password" userDataValue="●●●●●●●●●●●●" />

              <Stack
                sx={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}
              >
                <label htmlFor="upload-image">
                  <Button sx={{ width: 150 }} variant="contained" component="span">
                    Select avatar
                  </Button>
                  <input
                    id="upload-image"
                    hidden
                    accept=".jpg,.png,.gif"
                    type="file"
                    onChange={UploadAvatarHandler}
                  />
                </label>

                <Button
                  sx={{ width: 150 }}
                  variant="outlined"
                  onClick={() => dispatch(logoutUser())}
                >
                  Log out
                </Button>
              </Stack>
            </Stack>
            <Typography variant="h4">Favorite films</Typography>
            <FilmCardList films={favoriteFilms} key={100} />
          </>
        )}
      </Stack>
    </React.Fragment>
  )

  return <React.Fragment>{isAuth && user ? renderProfile() : <Navigate to="/" />}</React.Fragment>
}
