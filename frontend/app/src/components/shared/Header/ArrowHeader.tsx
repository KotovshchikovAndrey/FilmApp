import React from 'react';
import {AppBar, Toolbar} from "@mui/material";
import BackArrow from "../../BackArrow";

function ArrowHeader() {
    return (
        <React.Fragment>
            <AppBar position="sticky" color="inherit" elevation={0} sx={{my: 3}}>
                <Toolbar disableGutters>
                    <BackArrow/>
                </Toolbar>
            </AppBar>
        </React.Fragment>
    );
}

export default ArrowHeader;