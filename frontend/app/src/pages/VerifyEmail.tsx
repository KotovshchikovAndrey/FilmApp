import { verificationSchema, VerificationSchema } from "../helpers/validators"
import { Controller, useForm, useFormState } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import {Alert, Box, Button, CircularProgress, Container, Stack, TextField, Typography} from "@mui/material"
import { Navigate, useNavigate } from "react-router-dom"
import React from "react"

import api from "../api"
import { AxiosError } from "axios"
import { useAppDispatch, useAppSelector } from "../store"
import { verifyUser } from "../store/actionCreators"
import { authActions } from "../store/authReducer"
import ArrowHeader from "../components/shared/Header/ArrowHeader";

export function VerifyEmail() {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const user = useAppSelector((state) => state.auth.user)
  const isLoading = useAppSelector((state) => state.auth.loading)
  const userStatus = useAppSelector((state) => state.auth.status)
  const errorMessage = useAppSelector((state) => state.auth.errorMessage)

  const { handleSubmit, control } = useForm<VerificationSchema>({
    resolver: zodResolver(verificationSchema),
  })

  const { errors } = useFormState({ control })

  const onSubmit = async (data: VerificationSchema) => {
    dispatch(verifyUser(data.verificationCode))
  }

  React.useEffect(() => {
    if (userStatus === "active") navigate("/")

    dispatch(authActions.setErrorMessage(null))
  }, [userStatus])

  const renderPage = () => (
    <React.Fragment>
      <ArrowHeader />
      <Container maxWidth="xs">
        <form onSubmit={handleSubmit(onSubmit)}>
          <Stack spacing={3} mt={10}>
            <Typography variant="h5">Enter verification code</Typography>
            <Typography>
              A verification code has been sent to {user?.email}.<br />
              Please enter it to verify your email
            </Typography>
            <Controller
              control={control}
              name="verificationCode"
              render={({ field }) => (
                <TextField
                  variant="outlined"
                  fullWidth
                  id="verificationCode"
                  label="Verification code"
                  name="verificationCode"
                  onChange={(e) => field.onChange(e)}
                  value={field.value}
                  error={!!errors.verificationCode?.message}
                  helperText={errors.verificationCode?.message}
                />
              )}
            />
            {errorMessage !== null && <Alert severity="error">{errorMessage}</Alert>}
            <Button type="submit" variant="contained">
              Verify
            </Button>
            {isLoading && (
                <Box display="flex" justifyContent="center">
                  <CircularProgress size={60} />
                </Box>
            )}
          </Stack>
        </form>
      </Container>
    </React.Fragment>
  )

  return isAuth ? renderPage() : <Navigate to="/" />
}
