import React from "react"
import {IFilm} from "../../../core/entities"
import FilmCardItem from "./FilmCardItem"
import Grid from '@mui/material/Unstable_Grid2';

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
            <Grid container spacing={2}>
                {films.map((film: filmCardItem) => (
                    <Grid xs={6} sm={4} md={3}>
                        <FilmCardItem
                            title={film.title}
                            description={film.description}
                            isAdult={film.isAdult}
                        />
                    </Grid>
                ))}
            </Grid>
        </React.Fragment>
    )
}
