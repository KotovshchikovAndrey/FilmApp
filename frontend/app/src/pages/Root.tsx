import {Container} from "@mui/material";
import React from "react";
import {Outlet} from "react-router-dom";
import {WarnHeader} from "../components/shared/Header/WarnHeader";
import ScrollToTop from "../components/ScrollToTop";

export default function Root() {
    return (
        <React.Fragment>
            <WarnHeader />
            <Container sx={{mb: 10}}>
                <Outlet/>
            </Container>
          <ScrollToTop/>
        </React.Fragment>
    );
}