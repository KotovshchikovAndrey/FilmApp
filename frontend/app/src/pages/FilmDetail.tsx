import { Box, Button, Stack, Typography } from "@mui/material"
import * as React from "react"
import ArrowBackIcon from "@mui/icons-material/ArrowBack"
import AddCircleIcon from "@mui/icons-material/AddCircle"
import { Link, useParams } from "react-router-dom"

export default function FilmDetail() {
  const { filmId } = useParams()

  return (
    <React.Fragment>
      <Stack
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        maxWidth="md"
        sx={{
          margin: "0 auto",
        }}
      >
        <Link to={"/"} style={{ textDecoration: "none", alignSelf: "flex-start", color: "black" }}>
          <ArrowBackIcon fontSize="large" sx={{ marginTop: 3, cursor: "pointer" }} />
        </Link>
        <Box
          mb={1.5}
          sx={{
            background: "url('https://i.ytimg.com/vi/MxjjLp2NF4U/maxresdefault.jpg')",
            backgroundSize: "cover",
            backgroundRepeat: "no-repeat",
            backgroundPosition: "center",
            width: 400,
            height: 600,
          }}
        />
        <Box>
          <Typography width={500} fontSize={25} textAlign="center" mb={5}>
            Светит дюралайт - это гигабайт!
          </Typography>
        </Box>
        <Button
          variant="outlined"
          sx={{
            color: "purple",
            borderColor: "purple",
            "&:hover": {
              color: "purple",
              borderColor: "purple",
              background: "none",
            },
            marginBottom: 5,
          }}
        >
          <AddCircleIcon sx={{ marginRight: 1.5 }} />
          Добавить в коллекцию {filmId}
        </Button>
        <Box alignSelf="flex-start" mb={5}>
          <Typography fontSize={25} fontWeight="bold" mb={1}>
            Описание
          </Typography>
          <Typography fontSize={25}>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Corrupti vero impedit
            dignissimos itaque nam expedita? Inventore tempora praesentium maxime, nesciunt nemo
            repudiandae soluta doloribus vero explicabo aliquid quod, nam ullam.
          </Typography>
        </Box>
        <Box alignSelf="flex-start">
          <Typography fontSize={25} fontWeight="bold" mb={1}>
            Трейлер
          </Typography>
          <iframe
            width="560"
            height="315"
            src="https://www.youtube.com/embed/wyO8xy7fnBg" // Своя ссылка
            title="YouTube video player" // Свое название
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowFullScreen
          />
        </Box>
      </Stack>
    </React.Fragment>
  )
}
