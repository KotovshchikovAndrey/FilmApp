import {Container, Stack, Typography} from "@mui/material";
import Header from "../components/shared/Header";
import FilmSearchInput from "../components/shared/film/FilmSearchInput";
import FilmFilters from "../components/shared/film/FilmFilters";
import FilmCardList from "../components/shared/film/FilmCardList";
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