import { Box, Typography, Autocomplete, TextField } from "@mui/material"
import React from "react"

export default function FilmFilters() {
  return (
    <React.Fragment>
      <Box sx={{ display: "flex" }} pl={3} mb={3}>
        <Autocomplete
          disablePortal
          id="combo-box-demo"
          options={["драма", "комедия", "супергероика"]} // потом поместим массив из жанров, который возьмем с бэка
          sx={{ width: 300 }}
          onSelect={(event: React.ChangeEvent<HTMLInputElement>) => console.log(event.target.value)}
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
    </React.Fragment>
  )
}
