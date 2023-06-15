import React, {useState} from "react"
import Card from "@mui/material/Card"
import CardMedia from "@mui/material/CardMedia"
import {Link} from "react-router-dom"
import {CardActionArea, Skeleton} from "@mui/material"
import AspectRatio from "@mui/joy/AspectRatio"
import Tilt from "react-parallax-tilt"
import {API_URL} from "../../../core/config";

interface FilmCardItemProps {
  id: number
  title: string
  posterUrl: string
}

export default function FilmCardItem(props: FilmCardItemProps) {
  return (
    <React.Fragment>
        <Tilt tiltReverse>
          <Card elevation={0}>
            <Link to={`/film/${props.id}`}>
              <CardActionArea>
                <AspectRatio ratio={2 / 3}>
                  <CardMedia>
                    <img
                      loading="lazy"
                      src={props.posterUrl}
                      srcSet={props.posterUrl}
                      alt=""
                    />
                  </CardMedia>
                </AspectRatio>
              </CardActionArea>
            </Link>
          </Card>
        </Tilt>

    </React.Fragment>
  )
}
