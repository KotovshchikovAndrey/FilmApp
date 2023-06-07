import React, { FC, useEffect } from "react"
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Container,
  Stack,
  TextField,
  Typography,
} from "@mui/material"
import { loginSchema } from "../helpers/validators"
import { Controller, useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { ILoginRequest } from "../core/entities"
import { loginUser } from "../store/actionCreators"
import { useAppDispatch, useAppSelector } from "../store"
import { useNavigate } from "react-router-dom"
import { authActions } from "../store/authReducer"
import ArrowHeader from "../components/shared/Header/ArrowHeader"

const Login: FC = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const isLoading = useAppSelector((state) => state.auth.loading)
  const errorMessage = useAppSelector((state) => state.auth.errorMessage)

  const {
    handleSubmit,
    formState: { errors },
    control,
  } = useForm<ILoginRequest>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  })

  React.useEffect(() => {
    if (isAuth) navigate("/")

    // Сбрасываю сообщение об ошибке при каждом рендере
    dispatch(authActions.setErrorMessage(null))
  }, [isAuth])

  const onSubmit = (data: ILoginRequest) => {
    dispatch(loginUser(data))
  }

  return (
    <React.Fragment>
      <ArrowHeader />
      <Container maxWidth="xs">
        <form onSubmit={handleSubmit(onSubmit)}>
          <Stack spacing={3} mt={10} useFlexGap>
            <Typography variant="h5">Log in</Typography>
            <Controller
              control={control}
              name="email"
              render={({ field }) => (
                <TextField
                  autoFocus
                  variant="outlined"
                  fullWidth
                  id="email"
                  label="Email Address"
                  error={!!errors.email?.message}
                  helperText={errors.email?.message}
                  {...field}
                />
              )}
            />
            <Controller
              control={control}
              name="password"
              render={({ field }) => (
                <TextField
                  variant="outlined"
                  fullWidth
                  id="password"
                  label="Password"
                  type="password"
                  error={!!errors.password?.message}
                  helperText={errors.password?.message}
                  {...field}
                />
              )}
            />
            <Button type="submit" variant="contained">
              Log in
            </Button>
            {errorMessage !== null && <Alert severity="error">{errorMessage}</Alert>}
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
}
export default Login
