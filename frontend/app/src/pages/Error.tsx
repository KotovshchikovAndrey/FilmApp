import { useRouteError } from "react-router-dom";
import {Container, Typography} from "@mui/material";

export default function Error() {
    const error: any = useRouteError();
    console.error(error);

    return (
        <Container sx={{mt:10}}>
            <Typography variant="h2">
                Oops!
            </Typography>
            <Typography variant="h5">
                Sorry, an unexpected error has occurred.
            </Typography>
            <Typography variant="h1">
                {`${error.status } ${error.statusText || error.message}`}
            </Typography>
        </Container>
    );
}