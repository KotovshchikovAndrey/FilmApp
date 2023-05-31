import {Container} from "@mui/material";
import React from "react";
import {Outlet} from "react-router-dom";

export default function Root() {
    return (
        <React.Fragment>
            <Container>
                <Outlet/>
            </Container>
        </React.Fragment>
    );
}