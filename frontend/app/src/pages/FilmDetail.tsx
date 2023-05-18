import {Button, Container, Stack, Typography} from "@mui/material"
import * as React from "react"
import BackArrow from "../components/BackArrow"
import {useParams} from "react-router-dom"
import Grid from "@mui/material/Unstable_Grid2";
import {Chip} from "@mui/material";
import {Add} from "@mui/icons-material";
import AspectRatio from "@mui/joy/AspectRatio";

export default function FilmDetail() {
    const {filmId} = useParams()

    return (
        <React.Fragment>
            <Container>
                <BackArrow/>
                <Grid container spacing={5}>
                    <Grid xs={12} sm={6}>
                        <img style={{maxWidth: "100%"}}
                             src="https://avatars.mds.yandex.net/get-kinopoisk-image/1900788/41daf06f-3187-4913-98aa-f72f77544d8f/orig"
                             alt="aboba"
                        />
                    </Grid>
                    <Grid xs={12} sm={6}>
                        <Stack spacing={2}>
                            <Typography variant="h4" component="h1">
                                Название фильма #{filmId}
                            </Typography>
                            <Typography variant="subtitle1">
                                1999, США, 3ч 9мин 18+
                            </Typography>
                            <Stack direction="row" spacing={1} useFlexGap flexWrap="wrap">
                                <Chip label="Драма"/>
                                <Chip label="Комедия"/>
                                <Chip label="Криминал"/>
                                <Chip label="Криминал"/>
                                <Chip label="Криминал"/>
                                <Chip label="Криминал"/>
                                <Chip label="Криминал"/>
                                <Chip label="Криминал"/>
                                <Chip label="Криминал"/>
                                <Chip label="Криминал"/>
                                <Chip label="Криминал"/>
                                <Chip label="Криминал"/>
                            </Stack>
                            <Button variant="outlined" startIcon={<Add/>}>
                                Add to collection
                            </Button>
                            <Typography variant="h5">
                                Description
                            </Typography>
                            <Typography>
                                Lorem ipsum dolor sit amet consectetur adipisicing elit. Corrupti vero impedit
                                dignissimos itaque nam expedita? Inventore tempora praesentium maxime, nesciunt nemo
                                repudiandae soluta doloribus vero explicabo aliquid quod, nam ullam.
                            </Typography>
                            <Typography variant="h5">
                                Trailer
                            </Typography>
                            <AspectRatio>
                                <iframe
                                    src="https://www.youtube.com/embed/wyO8xy7fnBg" // Своя ссылка
                                    title="YouTube video player" // Свое название
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                    allowFullScreen
                                />
                            </AspectRatio>
                        </Stack>
                    </Grid>
                </Grid>
            </Container>

        </React.Fragment>
    )
}
