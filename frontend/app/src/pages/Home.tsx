import React from "react"
import { Box, CircularProgress, Stack, Typography } from "@mui/material"
import FilmSearchInput from "../components/shared/film/FilmSearchInput"
import FilmCardList from "../components/shared/film/FilmCardList"
import FilmFilters from "../components/shared/film/FilmFilters"
import ProfileHeader from "../components/shared/Header/ProfileHeader"
import FilmCollection from "../components/FilmCollection";

export default function Home() {

  return (
    <React.Fragment>
      <ProfileHeader />
      <Stack spacing={5} mb={10} mt={20}>
        <Typography variant="h4" component="h1">
          Опиши фильм, а мы подберем что-то подходящее :)
        </Typography>
        <FilmSearchInput />
      </Stack>
      <Stack spacing={3} mb={10} useFlexGap>
        <Typography variant="h5" component="h2">
          Коллекция
        </Typography>
        <FilmCollection/>
      </Stack>
    </React.Fragment>
  )
}
