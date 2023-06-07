import { verificationSchema, VerificationSchema } from "../helpers/validators"
import { Controller, useForm, useFormState } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Button, Container, Stack, TextField, Typography } from "@mui/material"
import { useNavigate } from "react-router-dom"
import React from "react"

import api from "../api"
import { AxiosError } from "axios"

export function VerifyEmail() {
  const navigate = useNavigate()
  const [apiErrorMessage, setApiErrorMessage] = React.useState("")

  const { handleSubmit, control } = useForm<VerificationSchema>({
    resolver: zodResolver(verificationSchema),
  })

  const { errors } = useFormState({ control })

  const onSubmit = async (data: VerificationSchema) => {
    const code = data.verificationCode
    try {
      await api.auth.redeemCode(code)
      navigate("/")
    } catch (err) {
      if (err instanceof AxiosError && err.response) {
        const apiErrorData = err.response.data
        setApiErrorMessage(apiErrorData.message)
      }
    }
  }

  return (
    <React.Fragment>
      <Container maxWidth="xs">
        <form onSubmit={handleSubmit(onSubmit)}>
          <Stack spacing={3} mt={10}>
            <Typography variant="h5">Enter verification code</Typography>
            <Typography>
              A verification code has been sent to {}.<br />
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
                  error={!!errors.verificationCode?.message || !!apiErrorMessage}
                  helperText={errors.verificationCode?.message ?? apiErrorMessage}
                />
              )}
            />
            <Button type="submit" variant="contained">
              Verify
            </Button>
          </Stack>
        </form>
      </Container>
    </React.Fragment>
  )
}
