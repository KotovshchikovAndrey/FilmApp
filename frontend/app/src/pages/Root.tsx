import {Container} from "@mui/material";
import React from "react";
import {Outlet} from "react-router-dom";
import {WarnHeader} from "../components/shared/Header/WarnHeader";

export default function Root() {
    return (
        <React.Fragment>
            <WarnHeader />
            <Container sx={{mb: 10}}>
                <Outlet/>
            </Container>
        </React.Fragment>
    );
}