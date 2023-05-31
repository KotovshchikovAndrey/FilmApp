import {AppBar, Button, Skeleton, Stack, Toolbar} from "@mui/material";
import LoginIcon from '@mui/icons-material/Login';
import {Link} from "react-router-dom";
import {AccountCircle} from "@mui/icons-material";
import {useSelector} from "react-redux";
import {IRootState, useAppSelector} from "../../store";
import React, {useEffect} from "react";

export default function Header() {
    const isLoggedIn = useAppSelector(state => !!state.auth.authData.accessToken)
    const userName = useAppSelector(state => state.auth.profileData.profile?.name)
    return (
        <React.Fragment>
            <AppBar position="static" color="transparent" elevation={0}>
                <Toolbar disableGutters>
                    <Stack direction="row" spacing={4} sx={{ml: 'auto'}}>
                        {isLoggedIn
                            ?
                            <Link to="/profile"><Button variant="text" startIcon={<AccountCircle/>}>{userName}</Button>
                            </Link>
                            :
                            <>
                                <Link to="/login">
                                    <Button variant="text" startIcon={<LoginIcon/>}>Login</Button>
                                </Link>
                                <Link to={`/register`}>
                                    <Button variant="outlined">Sign up</Button>
                                </Link>
                            </>
                        }
                    </Stack>

                </Toolbar>
            </AppBar>
        </React.Fragment>
    )
}