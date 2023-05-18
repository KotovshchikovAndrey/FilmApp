import React from "react"
import {Stack, Typography, Container} from "@mui/material"
import FilmSearchInput from "../components/shared/film/FilmSearchInput"
import FilmCardList from "../components/shared/film/FilmCardList"
import FilmFilters from "../components/shared/film/FilmFilters"

export default function Home() {
  return (
    <React.Fragment>
      <Container>
          <Stack spacing={5} mb={10} mt={20}>
              <Typography variant="h4" component="h1">
                  Опиши фильм, а мы подберем что-то подходящее :)
              </Typography>
              <FilmSearchInput/>
          </Stack>
          <Stack spacing={3} mb={10} useFlexGap>
              <Typography variant="h5" component="h2">Коллекция</Typography>
              <FilmFilters />
              <FilmCardList />
          </Stack>
      </Container>
    </React.Fragment>
  )
}
