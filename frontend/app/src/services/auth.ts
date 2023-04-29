import ky from "ky"
import { User } from "../core/entities"

interface IAuthService {
  register: () => User
  login: () => User
  logout: () => void
  resetPassword: () => void
}

// class AuthService implements IAuthService {}
