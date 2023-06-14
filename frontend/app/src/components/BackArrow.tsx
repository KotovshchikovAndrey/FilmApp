import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import {Link} from "react-router-dom";
import React from "react";
import {IconButton} from "@mui/material";

export default function BackArrow() {
    return (
        <React.Fragment>
            <Link to={".."}>
                <IconButton aria-label="back arrow" size="large">
                    <ArrowBackIcon fontSize="inherit"/>
                </IconButton>
            </Link>
        </React.Fragment>
    )
}