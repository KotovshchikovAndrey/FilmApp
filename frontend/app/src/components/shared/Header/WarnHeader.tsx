import React from "react";
import { useAppSelector } from "../../../store";
import { AppBar, Toolbar, Typography, Box, Button } from '@mui/material';
import { orange } from '@mui/material/colors';
import { useLocation, useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import api from "../../../api";


export function WarnHeader() {
    const isAuth = useAppSelector(state => state.auth.isAuth);
    const location = useLocation();
    const navigate = useNavigate();
    if (!isAuth || location.pathname.match(/^\/$|^\/profile$|^\/film\/[0-9]+$/) === null) return null;
    let msg;
    let need_button;
    switch (Cookies.get("status")) {
        case "not_verified":
            msg = "Your account isn't verified. Verify it as soon as possible.";
            need_button = true;
            break;
        case "muted":
            msg = "You have been muted.";
            need_button = false;
            break;
        default:
            return null;
    }

    const handleButtonClick = async () => {
        try {
            await api.auth.requestCode();
            navigate('/verify');
        } catch (error) {
            console.error("There was an error!", error);
        }
    };

    return (
        <React.Fragment>
            <AppBar position="static" style={{ backgroundColor: orange[500]}} elevation={0}>
                <Toolbar>
                    <Box sx={{ flexGrow: 1, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                        <Typography variant="body1" color="inherit" sx={{ textAlign: 'center' }}>
                            {msg}
                        </Typography>
                        {need_button && <Button variant="outlined" color="inherit" onClick={handleButtonClick} sx={{ ml: 2 }}>
                            Verify account
                        </Button>
                        }
                    </Box>
                </Toolbar>
            </AppBar>
        </React.Fragment>
    )
}