import React from "react"
import {AppBar, Box, Button, Stack, Toolbar} from "@mui/material";
import LoginIcon from '@mui/icons-material/Login';
import {Link} from "react-router-dom";

export default function TopAppBar() {
    return (
        <React.Fragment>
            <AppBar position="static" color="transparent" elevation={0}>
                <Toolbar disableGutters>
                    <Stack direction="row" spacing={4} sx={{ml: 'auto'}}>
                        <Link
                            to="/login"
                            style={{textDecoration: "none"}}
                        >
                            <Button variant="text" startIcon={<LoginIcon/>}>Login</Button>
                        </Link>
                        <Link
                            to={`/register`}
                            style={{textDecoration: "none"}}
                        >
                            <Button variant="outlined">Sign up</Button>
                        </Link>
                    </Stack>

                </Toolbar>
            </AppBar>
        </React.Fragment>
    )
}