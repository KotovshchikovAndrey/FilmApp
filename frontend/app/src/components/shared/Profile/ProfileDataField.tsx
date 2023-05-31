import React from 'react';
import {Divider, Typography} from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2";

interface ProfileDataFieldProps {
    userDataName: string;
    userDataValue: string;
}

const ProfileDataField = ({userDataName, userDataValue}: ProfileDataFieldProps) => {
    return (
        <React.Fragment>
            <Grid container>
                <Grid xs={6}>
                    <Typography>{userDataName}</Typography>
                </Grid>
                <Grid xs={6}>
                    <Typography>{userDataValue}</Typography>
                </Grid>
            </Grid>
            <Divider />
        </React.Fragment>
    );
};

export default ProfileDataField;