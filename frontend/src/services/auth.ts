import type { LoginSchema, UsuarioSchema } from "../types";
import { api } from "./api";

export const cadastrarAPI = (usuario: UsuarioSchema) => api.post("/auth/cadastrar", usuario)
export const loginAPI = (login: LoginSchema) => api.post("/auth/login", login)