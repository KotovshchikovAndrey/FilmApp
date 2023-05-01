import React from "react"
import { Stack, Container, Box } from "@mui/material"
import { IFilm } from "../../../core/entities"
import FilmCardItem from "./FilmCardItem"

export default function FilmCardList() {
  // Данные потом будем брать с бэка (эти для тестирования)
  type filmCardItem = Pick<IFilm, "id" | "title" | "description" | "isAdult">
  const films: filmCardItem[] = [
    {
      id: 1,
      title: "test1",
      description: "teghbjnsnnsnknsnnsnnnnnnnnnnnn...",
      isAdult: false,
    },
    {
      id: 2,
      title: "test2",
      description: "teghbjnsnnsnknsnnsnnnnnnnnnnnn...",
      isAdult: false,
    },
    {
      id: 3,
      title: "test3",
      description: "teghbjnsnnsnknsnnsnnnnnnnnnnnn...",
      isAdult: false,
    },
    {
      id: 1,
      title: "test1",
      description: "teghbjnsnnsnknsnnsnnnnnnnnnnnn...",
      isAdult: false,
    },
    {
      id: 2,
      title: "test2",
      description: "teghbjnsnnsnknsnnsnnnnnnnnnnnn...",
      isAdult: false,
    },
    {
      id: 3,
      title: "test3",
      description: "teghbjnsnnsnknsnnsnnnnnnnnnnnn...",
      isAdult: false,
    },
    {
      id: 1,
      title: "test1",
      description: "teghbjnsnnsnknsnnsnnnnnnnnnnnn...",
      isAdult: false,
    },
    {
      id: 2,
      title: "test2",
      description: "teghbjnsnnsnknsnnsnnnnnnnnnnnn...",
      isAdult: false,
    },
    {
      id: 3,
      title: "test3",
      description: "teghbjnsnnsnknsnnsnnnnnnnnnnnn...",
      isAdult: false,
    },
  ]

  return (
    <React.Fragment>
      <Container maxWidth="lg">
        <Stack direction="row" justifyContent="center" flexWrap="wrap">
          {films.map((film: filmCardItem) => (
            <Box m={3}>
              <FilmCardItem
                title={film.title}
                description={film.description}
                isAdult={film.isAdult}
              />
            </Box>
          ))}
        </Stack>
      </Container>
    </React.Fragment>
  )
}
