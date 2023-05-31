import React from 'react';
import {AppBar, Toolbar} from "@mui/material";
import BackArrow from "../../BackArrow";

function ArrowHeader() {
    return (
        <React.Fragment>
            <AppBar position="static" color="transparent" elevation={0}>
                <Toolbar disableGutters>
                    <BackArrow/>
                </Toolbar>
            </AppBar>
        </React.Fragment>
    );
}

export default ArrowHeader;