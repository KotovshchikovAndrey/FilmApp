import React, {useEffect, useState} from "react"
import {Box, CircularProgress, Stack, Typography} from "@mui/material"
import FilmSearchInput from "../components/shared/film/FilmSearchInput"
import FilmCardList from "../components/shared/film/FilmCardList"
import FilmFilters from "../components/shared/film/FilmFilters"
import ProfileHeader from "../components/shared/Header/ProfileHeader";
import {useFilms} from "../hooks/films";


export default function Home() {
    const {films, loading, err} = useFilms()
    return (
        <React.Fragment>
            <ProfileHeader/>
            <Stack spacing={5} mb={10} mt={20}>
                <Typography variant="h4" component="h1">
                    Опиши фильм, а мы подберем что-то подходящее :)
                </Typography>
                <FilmSearchInput/>
            </Stack>
            <Stack spacing={3} mb={10} useFlexGap>
                 {/*TODO объединить заголовок, фильтры, тупой поиск и фильмы в один компонент*/}
                 {/*TODO заголовок списка фильмов в пропс, чтобы он был изменяемым*/}
                <Typography variant="h5" component="h2">Коллекция</Typography>
                <FilmFilters/>
                {/*TODO перенести loading в film card list 1:23:00*/}
                {loading ? <Box mt={10} display='flex' justifyContent="center"><CircularProgress size={100}/></Box>:
                <FilmCardList films={films}/>}
            </Stack>
        </React.Fragment>
    )
}
