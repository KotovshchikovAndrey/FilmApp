import React from "react"
import { Stack, Rating, Typography } from "@mui/material"
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
      <Stack spacing={1}>
        <Typography>AVG rating: {rating}</Typography>
        <Rating
          name="size-large"
          size="large"
          defaultValue={props.userRating}
          precision={0.5}
          onChange={(event, newValue) => setRatingHandler(newValue)}
        />
      </Stack>
    </React.Fragment>
  )
}
