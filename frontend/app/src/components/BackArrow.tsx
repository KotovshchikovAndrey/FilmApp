import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import {Link} from "react-router-dom";
import React from "react";
import {IconButton} from "@mui/material";

export default function BackArrow() {
    return (
        <React.Fragment>
            <Link to={".."} style={{marginTop: 10}}>
                <IconButton aria-label="back arrow">
                    <ArrowBackIcon/>
                </IconButton>
            </Link>
        </React.Fragment>
    )
}