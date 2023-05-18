import React from "react"
import Card from "@mui/material/Card"
import CardMedia from "@mui/material/CardMedia"
import {Link} from "react-router-dom"
import {CardActionArea} from "@mui/material";
import AspectRatio from '@mui/joy/AspectRatio';
import Tilt from 'react-parallax-tilt';

interface FilmCardItemProps {
    title: string
    description?: string
    isAdult: boolean
    posterUrl?: string
}

export default function FilmCardItem(props: FilmCardItemProps) {
    return (
        <React.Fragment>
            <Tilt tiltReverse>
                <Card elevation={0}>
                    <Link
                        to={`/${Math.ceil(Math.random() * 100)}`} // Потом добавим id с бэка (динамику)*/
                    >
                        <CardActionArea>
                            <AspectRatio ratio={2 / 3}>
                                <CardMedia
                                    component="img"
                                    image="https://i.ytimg.com/vi/9wOiUI6FGEo/maxresdefault.jpg" // Потом заменим на свою
                                    alt={props.title}
                                />
                            </AspectRatio>
                        </CardActionArea>
                    </Link>
                </Card>
            </Tilt>
        </React.Fragment>
    )
}
