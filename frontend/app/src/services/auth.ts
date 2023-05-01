import ky from "ky"
import { IUser } from "../core/entities"

interface IAuthService {
  register: () => IUser
  login: () => IUser
  logout: () => void
  resetPassword: () => void
}

// class AuthService implements IAuthService {}
