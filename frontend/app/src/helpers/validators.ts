import * as zod from "zod"

export const registerSchema = zod.object({
  email: zod.string().email("Invalid email address"),
  password: zod
    .string()
    .min(8, "Must be 8 or more characters long")
    .max(100, "Must be 100 or fewer characters long"),
  name: zod
    .string()
    .min(1, "This field is required")
    .max(30, "Must be 30 or fewer characters long"),
  surname: zod
    .string()
    .min(1, "This field is required")
    .max(30, "Must be 30 or fewer characters long"),
})

export const loginSchema = zod.object({
  email: zod.string().email("Invalid email address"),
  password: zod
    .string()
    .min(8, "Must be 8 or more characters long")
    .max(100, "Must be 100 or fewer characters long"),
})

export const verificationSchema = zod.object({
  verificationCode: zod.string().regex(/\d{5}/, "code must be number length 5").length(5),
})

export type VerificationSchema = zod.infer<typeof verificationSchema>
