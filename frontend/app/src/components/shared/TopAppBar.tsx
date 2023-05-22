import React, {useContext} from "react"
import {AppBar, Box, Button, Stack, Toolbar} from "@mui/material";
import LoginIcon from '@mui/icons-material/Login';
import {Link} from "react-router-dom";
import {Context} from "../../index";
import {AccountCircle} from "@mui/icons-material";

export default function TopAppBar() {
    const {store} = useContext(Context)
    return (
        <React.Fragment>
            <AppBar position="static" color="transparent" elevation={0}>
                <Toolbar disableGutters>
                    <Stack direction="row" spacing={4} sx={{ml: 'auto'}}>
                        {store.isAuth ?
                            <Link to="/profile"><Button variant="text" startIcon={<AccountCircle/>}>Профиль</Button>
                            </Link> :
                            <>
                                <Link to="/login">
                                    <Button variant="text" startIcon={<LoginIcon/>}>Login</Button>
                                </Link>
                                <Link to={`/register`}>
                                    <Button variant="outlined">Sign up</Button>
                                </Link>
                            </>}
                    </Stack>

                </Toolbar>
            </AppBar>
        </React.Fragment>
    )
}