import {Autocomplete, TextField} from "@mui/material"
import React from "react"
import Grid from "@mui/material/Unstable_Grid2";

export default function FilmFilters() {
    return (
        <React.Fragment>
            <Grid container spacing={2}>
                <Grid xs={12} md>
                    <Autocomplete
                        size="small"
                        disablePortal
                        id="combo-box-demo"
                        options={["драма", "комедия", "супергероика"]} // потом поместим массив из жанров, который возьмем с бэка
                        onSelect={(event: React.ChangeEvent<HTMLInputElement>) => console.log(event.target.value)}
                        renderInput={(params) => <TextField {...params} label="Жанр"/>}
                    />
                </Grid>
                <Grid xs={12} md>
                    <Autocomplete
                        size="small"
                        disablePortal
                        id="combo-box-demo"
                        options={[]} // потом поместим массив из стран, который возьмем с бэка
                        renderInput={(params) => <TextField {...params} label="Страна"/>}
                    />
                </Grid>
            </Grid>
        </React.Fragment>
    )
}
