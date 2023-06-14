import {AppBar, Avatar, Button, Icon, IconButton, Stack, Toolbar} from "@mui/material"
import LoginIcon from "@mui/icons-material/Login"
import { Logout } from "@mui/icons-material"
import { Link } from "react-router-dom"
import { AccountCircle } from "@mui/icons-material"
import { useAppSelector, useAppDispatch } from "../../../store"
import { logoutUser } from "../../../store/actionCreators"
import React from "react"
import {API_URL} from "../../../core/config";

export default function ProfileHeader() {
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const user = useAppSelector((state) => state.auth.user)

  return (
    <React.Fragment>
      <AppBar position="static" color="transparent" elevation={0}>
        <Toolbar disableGutters>
          <Stack direction="row" spacing={4} ml="auto" mt={3}>
            {isAuth && user ? (
              <>
                <Link to="/profile">
                  <IconButton>
                    <Avatar
                      src={
                        user.avatar
                          ? `${API_URL}/users/media` + user.avatar
                          : "https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"
                      }
                      sx={{ width: 48, height: 48 }}
                    />
                  </IconButton>
                </Link>
                {/*<Button*/}
                {/*  variant="text"*/}
                {/*  startIcon={<Logout />}*/}
                {/*  onClick={() => dispatch(logoutUser())}*/}
                {/*>*/}
                {/*  Logout*/}
                {/*</Button>*/}
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="text" startIcon={<LoginIcon />}>
                    Login
                  </Button>
                </Link>
                <Link to={`/register`}>
                  <Button variant="outlined">Sign up</Button>
                </Link>
              </>
            )}
          </Stack>
        </Toolbar>
      </AppBar>
    </React.Fragment>
  )
}
