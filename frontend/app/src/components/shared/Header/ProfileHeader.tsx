import { AppBar, Button, Stack, Toolbar } from "@mui/material"
import LoginIcon from "@mui/icons-material/Login"
import { Logout } from "@mui/icons-material"
import { Link } from "react-router-dom"
import { AccountCircle } from "@mui/icons-material"
import { useAppSelector, useAppDispatch } from "../../../store"
import { logoutUser } from "../../../store/actionCreators"
import React from "react"

export default function ProfileHeader() {
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const user = useAppSelector((state) => state.auth.user)

  return (
    <React.Fragment>
      <AppBar position="static" color="transparent" elevation={0}>
        <Toolbar disableGutters>
          <Stack direction="row" spacing={4} sx={{ ml: "auto" }}>
            {isAuth && user ? (
              <>
                <Link to="/profile">
                  <Button variant="text" startIcon={<AccountCircle />}>
                    {`${user.name} ${user.surname}`}
                  </Button>
                </Link>
                <Button
                  variant="text"
                  startIcon={<Logout />}
                  onClick={() => dispatch(logoutUser())}
                >
                  Logout
                </Button>
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
