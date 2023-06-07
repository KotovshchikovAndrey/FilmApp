import React from 'react';
import AspectRatio from "@mui/joy/AspectRatio";
import {Skeleton} from "@mui/material";
import {IFilm} from "../../../core/entities";
import Grid from "@mui/material/Unstable_Grid2";
import FilmCardItem from "./FilmCardItem";

function FilmCardListSkeleton() {
  const getSkeletonCards = () => {
    let content = []
    for (let i = 0; i < 10; i++) {
      content.push(
        <Grid xs={6} sm={4} md={3}>
          <AspectRatio ratio={2 / 3}>
            <Skeleton variant="rectangular"/>
          </AspectRatio>
        </Grid>
      )
    }
    return content
  }
  return (
    <React.Fragment>
      <Grid container spacing={2}>
        {getSkeletonCards()}
    </Grid>

</React.Fragment>
)
  ;
}

export default FilmCardListSkeleton;