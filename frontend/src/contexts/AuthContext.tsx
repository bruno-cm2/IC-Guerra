import { createContext, useEffect, useState, type ReactNode } from "react";
import type { LoginSchema } from "../types";
import { getToken } from "../services/auth";
import { api } from "../services/api";

type AuthContextType = {
  user: LoginSchema | null
  loading: boolean
  setUser: (user: UsuarioSchema | null) => void
}

type Props ={
    children: ReactNode
}

export const AuthContext = createContext<AuthContextType | null>(null)

export const AuthProvider = ({children}: Props) =>{
    const [user, setUser] = useState<LoginSchema | null>(null)
    const [loading, setLoading] = useState<Boolean>(true)

    useEffect(() => {
        const token = getToken()
        if(token){
            api.post("/login")
        }
    })
}

