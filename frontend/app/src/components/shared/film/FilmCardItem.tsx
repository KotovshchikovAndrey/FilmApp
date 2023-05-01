import React from "react"
import Card from "@mui/material/Card"
import CardActions from "@mui/material/CardActions"
import CardContent from "@mui/material/CardContent"
import CardMedia from "@mui/material/CardMedia"
import Button from "@mui/material/Button"
import Typography from "@mui/material/Typography"

interface FilmCardItemProps {
  title: string
  description?: string
  isAdult: boolean
}

export default function FilmCardItem(props: FilmCardItemProps) {
  return (
    <React.Fragment>
      <Card sx={{ maxWidth: 300 }}>
        <CardMedia
          sx={{ height: 150 }}
          image="https://i.ytimg.com/vi/9wOiUI6FGEo/maxresdefault.jpg" // Потом заменим на свою
          title="green iguana"
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {props.title} {props.isAdult ? "18+" : "0+"}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {props.description}
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small">Подробнее</Button>
        </CardActions>
      </Card>
    </React.Fragment>
  )
}
