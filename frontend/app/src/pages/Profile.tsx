import * as React from "react"
import {Avatar, Box, Button, CircularProgress, Skeleton, Stack, TextField, Typography} from "@mui/material"
import {useAppDispatch, useAppSelector} from "../store"
import {Navigate} from "react-router-dom"
import {fetchUserFavoriteFilms, logoutUser, setUserAvatar} from "../store/actionCreators"
import ArrowHeader from "../components/shared/Header/ArrowHeader"
import ProfileDataField from "../components/shared/Profile/ProfileDataField"
import FilmCardList from "../components/shared/film/FilmCardList"
import {API_URL} from "../core/config"
import Grid from "@mui/material/Unstable_Grid2";
import EditIcon from '@mui/icons-material/Edit';
import LogoutIcon from '@mui/icons-material/Logout';
import UploadIcon from '@mui/icons-material/Upload';

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
      <ArrowHeader/>
      <Stack spacing={3} useFlexGap>
        <Button
          sx={{maxWidth: 150, alignSelf: "end"}}
          startIcon={<LogoutIcon/>}
          variant="outlined"
          onClick={() => dispatch(logoutUser())}
        >
          Log out
        </Button>
        {user !== null && (
          <>
            <Grid container spacing={2}>
              <Grid xs={12} md={4}>
                <Box maxWidth={200} mx="auto">
                  <Avatar
                    src={
                      user.avatar
                        ? `${API_URL}/users/media` + user.avatar
                        : "https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"
                    }
                    sx={{width: 200, height: 200}}
                  />
                </Box>

              </Grid>
              <Grid xs={6} md={4}>
                <Stack spacing={2}>
                  {/*<Typography variant="h4">{user.name} {user.surname}</Typography>*/}
                  {/*<Typography variant="body1">{user.name} {user.surname}</Typography>*/}
                  <TextField
                    InputProps={{
                      readOnly: true,
                    }}
                    label="Name"
                    defaultValue={user.name}
                  />
                  <TextField
                    InputProps={{
                      readOnly: true,
                    }}
                    label="Email"
                    defaultValue={user.email}
                  />
                  <label htmlFor="upload-image">
                    <Button variant="text" startIcon={<UploadIcon/>} component="span">
                      Upload avatar</Button>
                    <input
                      id="upload-image"
                      hidden
                      accept=".jpg,.png,.gif"
                      type="file"
                      onChange={UploadAvatarHandler}
                    />

                  </label>

                </Stack>
              </Grid>
              <Grid xs={6} md={4}>
                <Stack spacing={2}>
                  <TextField
                    InputProps={{
                      readOnly: true,
                    }}
                    label="Surname"
                    defaultValue={user.surname}
                  />
                  <TextField
                    InputProps={{
                      readOnly: true,
                    }}
                    label="Password"
                    defaultValue="●●●●●●●●●●●●"
                  />
                  <Button disabled sx={{maxWidth: 100, alignSelf: "end"}} variant="outlined"
                          startIcon={<EditIcon/>}>Edit</Button>
                </Stack>

              </Grid>
            </Grid>


            <Stack spacing={3} my={5} maxWidth={600} useFlexGap>

              <Stack
                sx={{display: "flex", flexDirection: "row", justifyContent: "space-between"}}
              >


              </Stack>
            </Stack>
            <Typography variant="h4">Favorite films</Typography>
            <FilmCardList films={favoriteFilms} key={100}/>
          </>
          )}
      </Stack>
    </React.Fragment>
)

return <React.Fragment>{isAuth && user ? renderProfile() : <Navigate to="/"/>}</React.Fragment>
}
