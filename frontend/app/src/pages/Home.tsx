import React from "react"
import { Stack, Typography, Box, Autocomplete, TextField } from "@mui/material"
import FilmSearchInput from "../components/shared/film/FilmSearchInput"
import FilmCardList from "../components/shared/film/FilmCardList"
import FilmFilters from "../components/shared/film/FilmFilters"

export default function Home() {
  return (
    <React.Fragment>
      <Stack
        maxWidth="lg"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        sx={{
          margin: "0 auto",
        }}
      >
        <Box mb={5}>
          <Typography variant="h4" component="h1" mb={5} mt={5} maxWidth={500}>
            Опиши фильм, а мы подберем что-то подходящее :)
          </Typography>
          <FilmSearchInput />
        </Box>
        <Box width={960}>
          <Typography variant="h4" component="h1" mb={2} mt={5} maxWidth={500} pl={3}>
            Коллекция
          </Typography>
          <FilmFilters />
          <FilmCardList />
        </Box>
      </Stack>
    </React.Fragment>
  )
}
