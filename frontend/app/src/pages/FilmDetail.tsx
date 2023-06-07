import {Box, Button, CircularProgress, Stack, Typography} from "@mui/material"
import * as React from "react"
import {useParams} from "react-router-dom"
import Grid from "@mui/material/Unstable_Grid2";
import {Chip} from "@mui/material";
import {Add} from "@mui/icons-material";
import AspectRatio from "@mui/joy/AspectRatio";
import ArrowHeader from "../components/shared/Header/ArrowHeader";
import {useFilms} from "../hooks/useFilms";
import {useFilmDetail} from "../hooks/filmDetail";
import {IGenre} from "../core/entities";

export default function FilmDetail() {
    const {id} = useParams()
    const filmId = parseInt(id!)
    // TODO разделить фетч фильма и трейлера на 2 useFetching
    const {film, loading, err} = useFilmDetail(filmId)
    return (
        <React.Fragment>
            <ArrowHeader/>
            {loading ? <Box mt={20} display='flex' justifyContent="center"><CircularProgress size={100}/></Box> :
            <Grid container spacing={5}>
                <Grid xs={12} sm={6}>
                    {/*TODO Размер фото*/}
                    <img style={{maxWidth: "100%"}}
                         src={film?.posterUrl}
                         alt={film?.title}
                    />
                </Grid>
                <Grid xs={12} sm={6}>
                    <Stack spacing={2}>
                        <Typography variant="h4" component="h1">
                            {film.title}
                        </Typography>
                        <Typography variant="subtitle1">
                            {film.release_date}, {film.time} мин, {film.isAdult ? '18+' : '0+'}
                        </Typography>
                        <Stack direction="row" spacing={1} useFlexGap flexWrap="wrap">
                            {film.genres?.map((genre: IGenre) => (
                                <Chip label={genre.name}/>
                            ))}
                        </Stack>
                        <Button variant="outlined" startIcon={<Add/>}>
                            Add to collection
                        </Button>
                        <Typography variant="h5">
                            Description
                        </Typography>
                        <Typography>
                            {film.description}
                        </Typography>
                        <Typography variant="h5">
                            Trailer
                        </Typography>
                        <AspectRatio>
                            <iframe
                                src={film.trailerUrl}
                                title={film.title}
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                allowFullScreen
                            />
                        </AspectRatio>
                    </Stack>
                </Grid>
            </Grid>}
        </React.Fragment>
    )
}
