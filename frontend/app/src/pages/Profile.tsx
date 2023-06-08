import * as React from "react"
import { Button, Skeleton, Stack, Typography } from "@mui/material"
import { useAppDispatch, useAppSelector } from "../store"
import { Navigate } from "react-router-dom"
import { fetchUserFavoriteFilms, logoutUser } from "../store/actionCreators"
import ArrowHeader from "../components/shared/Header/ArrowHeader"
import ProfileDataField from "../components/shared/Profile/ProfileDataField"
import FilmCardList from "../components/shared/film/FilmCardList"

export default function Profile() {
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const user = useAppSelector((state) => state.auth.user)

  const favoriteFilms = useAppSelector((state) => state.film.favoriteFilms)

  React.useEffect(() => {
    dispatch(fetchUserFavoriteFilms())
  }, [])

  const renderProfile = () => (
    <React.Fragment>
      <ArrowHeader />
      <Stack spacing={3} mt={5} useFlexGap>
        <Skeleton variant="text" sx={{ fontSize: "4rem" }} />
        <Skeleton variant="text" sx={{ fontSize: "2rem" }} />
        <Skeleton variant="text" sx={{ fontSize: "2rem" }} />
        <Skeleton variant="text" sx={{ fontSize: "2rem" }} />
        <Skeleton variant="text" sx={{ fontSize: "2rem" }} />
        {user !== null && (
          <>
            <Typography variant="h3">Welcome {user.name}</Typography>
            <Stack spacing={3} my={5} maxWidth={600} useFlexGap>
              <ProfileDataField userDataName="Name" userDataValue={user.name} />
              <ProfileDataField userDataName="Surname" userDataValue={user.surname} />
              <ProfileDataField userDataName="Email" userDataValue={user.email} />
              <ProfileDataField userDataName="Password" userDataValue="●●●●●●●●●●●●" />
              <Button
                sx={{ maxWidth: 150 }}
                variant="outlined"
                onClick={() => dispatch(logoutUser())}
              >
                Log out
              </Button>
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
