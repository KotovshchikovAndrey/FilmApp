import { Autocomplete, Box, TextField } from "@mui/material"
import React, { useEffect, useState } from "react"
import Grid from "@mui/material/Unstable_Grid2"
import api from "../../../api"
import { ICountry, IFilmFilter, IFilmFilterOptions, IGenre } from "../../../core/entities"
import { useAppDispatch, useAppSelector } from "../../../store"
import { filmActions } from "../../../store/filmReducer"
import { fetchFilms } from "../../../store/actionCreators"

export default function FilmFilters() {
  const dispatch = useAppDispatch()
  const filterValue = useAppSelector((state) => state.film.filter)
  const [filterOptions, setFilterOptions] = useState<IFilmFilterOptions>()
  // const [filterValue, setFilterValue] = useState<IFilmFilter>(InitialFilter)

  useEffect(() => {
    const fetchFilmFilterOptions = async () => {
      const response = await api.films.getFilmFilterOptions()
      setFilterOptions(response.data)
    }

    fetchFilmFilterOptions()
  }, [])

  const changeFilterHandler = (filter: IFilmFilter) => {
    dispatch(fetchFilms({ limit: 20, filter }))
  }

  return (
    <React.Fragment>
      <Grid container spacing={2}>
        <Grid xs={12} md>
          <Autocomplete
            size="small"
            disablePortal
            options={filterOptions ? filterOptions.genres : []}
            getOptionLabel={(option: IGenre) => option.name}
            // onSelect={(event: React.ChangeEvent<HTMLInputElement>) =>
            //   console.log(event.target.value)
            // }
            renderInput={(params) => <TextField {...params} label="Genre" />}
            value={filterValue.genre}
            // onChange={(event: any, newValue, reason) => {
            //   dispatch(filmActions.setFilter({ ...filterValue, genre: newValue }))
            // }}
            onChange={(event: any, newValue, reason) =>
              changeFilterHandler({ ...filterValue, genre: newValue })
            }
          />
        </Grid>
        <Grid xs={12} md>
          <Autocomplete
            size="small"
            disablePortal
            options={filterOptions ? filterOptions.countries : []}
            getOptionLabel={(option: ICountry) => option.name}
            renderInput={(params) => <TextField {...params} label="Country" />}
            renderOption={(props, option: ICountry) => (
              <Box component="li" sx={{ "& > img": { mr: 2, flexShrink: 0 } }} {...props}>
                <img
                  loading="lazy"
                  width="40"
                  src={`https://flagcdn.com/w40/${option.iso_3166_1.toLowerCase()}.png`}
                  srcSet={`https://flagcdn.com/w40/${option.iso_3166_1.toLowerCase()}.png 2x`}
                  alt=""
                />
                {option.name}
              </Box>
            )}
            value={filterValue.country}
            // onChange={(event: any, newValue, reason) => {
            //   dispatch(filmActions.setFilter({ ...filterValue, country: newValue }))
            // }}
            onChange={(event: any, newValue, reason) => {
              changeFilterHandler({ ...filterValue, country: newValue })
            }}
          />
        </Grid>
      </Grid>
    </React.Fragment>
  )
}
