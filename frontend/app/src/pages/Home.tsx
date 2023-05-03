import React from "react"
import { Stack, Typography, Box, Autocomplete, TextField } from "@mui/material"
import FilmSearchInput from "../components/shared/film/FilmSearchInput"
import FilmCardList from "../components/shared/film/FilmCardList"

export default function Home() {
  return (
    <React.Fragment>
      <Stack
        maxWidth="lg"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        sx={{
          // display: "flex",
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
          <Box sx={{ display: "flex" }} pl={3} mb={3}>
            <Autocomplete
              disablePortal
              id="combo-box-demo"
              options={["драма", "комедия", "супергероика"]} // потом поместим массив из жанров, который возьмем с бэка
              sx={{ width: 300 }}
              onSelect={(event: React.ChangeEvent<HTMLInputElement>) =>
                console.log(event.target.value)
              }
              renderInput={(params) => <TextField {...params} label="Жанр" />}
            />
            <Autocomplete
              disablePortal
              id="combo-box-demo"
              options={[]} // потом поместим массив из стран, который возьмем с бэка
              sx={{ width: 300 }}
              renderInput={(params) => <TextField {...params} label="Страна" />}
            />
          </Box>
          <FilmCardList />
        </Box>
      </Stack>
    </React.Fragment>
  )
}
