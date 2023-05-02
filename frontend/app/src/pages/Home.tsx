import React from "react"
import { Stack, Typography, Box } from "@mui/material"
import FilmSearchInput from "../components/shared/film/FilmSearchInput"

export default function Home() {
  return (
    <React.Fragment>
      <Stack direction="column" alignItems="center">
        <Box>
          <Typography variant="h4" component="h1" mb={5} mt={5} maxWidth={500}>
            Опиши фильм, а мы подберем что-то подходящее :)
          </Typography>
          <FilmSearchInput />
        </Box>
      </Stack>
    </React.Fragment>
  )
}
