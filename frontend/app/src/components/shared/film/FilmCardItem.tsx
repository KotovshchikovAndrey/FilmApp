import React from "react"
import Card from "@mui/material/Card"
import CardMedia from "@mui/material/CardMedia"
import { Link } from "react-router-dom"
import { CardActionArea } from "@mui/material"
import AspectRatio from "@mui/joy/AspectRatio"
import Tilt from "react-parallax-tilt"

interface FilmCardItemProps {
  id: number
  title: string
  posterUrl?: string
}

export default function FilmCardItem(props: FilmCardItemProps) {
  return (
    <React.Fragment>
      <Tilt tiltReverse>
        <Card elevation={0}>
          <Link to={`/film/${props.id}`}>
            <CardActionArea>
              <AspectRatio ratio={2 / 3}>
                <CardMedia component="img" image={props.posterUrl} alt={props.title} />
              </AspectRatio>
            </CardActionArea>
          </Link>
        </Card>
      </Tilt>
    </React.Fragment>
  )
}
