import React from "react"
import {Stack, Rating, Typography} from "@mui/material"
import api from "../../../api"

interface FilmStarRatingProps {
  filmId: number
  userRating: number
}

export const FilmStarRating: React.FC<FilmStarRatingProps> = (props: FilmStarRatingProps) => {
  const [rating, setRating] = React.useState(0)

  const setRatingHandler = async (ratingValue: number | null) => {
    if (ratingValue !== null) {
      const token = localStorage.getItem("token") as string
      await api.films.setFilmRating(props.filmId, ratingValue, token)
    }
  }

  React.useEffect(() => {
    const fetchFilmRating = async (filmId: number) => {
      const response = await api.films.getFilmRating(filmId)
      setRating(response.data.rating)
    }

    fetchFilmRating(props.filmId)
  }, [])

  return (
    <React.Fragment>
      <Stack spacing={3} direction="row" alignItems="center">
        <Stack alignItems="center">
          <Typography sx={{fontSize: 35, fontWeight: 900}}>{rating}/5</Typography>
          <Typography variant="subtitle2">Users rating</Typography>
        </Stack>
        <Stack>
          <Typography variant="h6">Rate</Typography>
          <Rating
            name="size-large"
            size="large"
            defaultValue={props.userRating}
            precision={0.5}
            onChange={(event, newValue) => setRatingHandler(newValue)}
          />

        </Stack>
      </Stack>
    </React.Fragment>
  )
}
