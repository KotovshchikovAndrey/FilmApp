import * as zod from "zod";

export const authSchema = zod.object({
    email: zod.string().email("Invalid email address"),
    password: zod.string().min(8, "Must be 8 or more characters long").max(32, "Must be 32 or fewer characters long"),
    name: zod.string().max(30, "Must be 30 or fewer characters long"),
    surname: zod.string().max(30, "Must be 30 or fewer characters long"),
});

export type AuthSchema = zod.infer<typeof authSchema>
