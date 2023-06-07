import { Autocomplete, TextField } from "@mui/material"
import React from "react"
import Grid from "@mui/material/Unstable_Grid2"

import api from "../../../api"
import { IFilmFilters } from "../../../core/entities"

export default function FilmFilters() {
  const [filters, setFilters] = React.useState<IFilmFilters>()

  React.useEffect(() => {
    const fetchFilmFilters = async () => {
      const response = await api.films.getFilmFilters()
      setFilters(response.data)
    }

    fetchFilmFilters()
  }, [])

  return (
    <React.Fragment>
      <Grid container spacing={2}>
        <Grid xs={12} md>
          <Autocomplete
            size="small"
            disablePortal
            id="combo-box-demo"
            options={filters ? filters.genres.map((genre) => genre.name) : []} // потом поместим массив из жанров, который возьмем с бэка
            // onSelect={(event: React.ChangeEvent<HTMLInputElement>) =>
            //   console.log(event.target.value)
            // }
            renderInput={(params) => <TextField {...params} label="Жанр" />}
          />
        </Grid>
        <Grid xs={12} md>
          <Autocomplete
            size="small"
            disablePortal
            id="combo-box-demo"
            options={filters ? filters.countries.map((country) => country.name) : []} // потом поместим массив из стран, который возьмем с бэка
            renderInput={(params) => <TextField {...params} label="Страна" />}
          />
        </Grid>
      </Grid>
    </React.Fragment>
  )
}
