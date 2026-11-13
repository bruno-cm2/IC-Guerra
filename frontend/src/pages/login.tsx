import { useState, type SubmitEvent } from "react";
import { Button, FloatingLabel, Form, FormControl } from "react-bootstrap";
import type { LoginSchema } from "../types";
import { loginAPI } from "../services/auth";
import axios from "axios";
import { useNavigate } from "react-router";

export const Login = () => {

    const navigate = useNavigate()
    const [error, setError] = useState<string>()

    const handleSubmit = async (event: SubmitEvent<HTMLFormElement>) => {
        event.preventDefault()

        const dados = new FormData(event.currentTarget)
        const login = Object.fromEntries(dados) as LoginSchema

        try{
            await loginAPI(login)
            navigate("/home")
        }
        catch(e){
            if (axios.isAxiosError(e)) {
                setError(e.response?.data?.detail ?? "Não foi possível conectar ao servidor")
            } else {
                setError("Erro inesperado")
            }
        }
    }
    
    return(
        <Form className="w-50 d-flex flex-column border rounded-5 shadow m-auto p-5 pt-4 gap-4"
        onSubmit={handleSubmit}>

            <h2 className="text-dark m-0">Acesse sua conta</h2>

            <FloatingLabel label="E-mail">
                <FormControl name="email" type="email" placeholder="E-mail" required />
            </FloatingLabel>

            <FloatingLabel label="Senha">
                <FormControl name="senha" type="password" placeholder="Senha" required />
            </FloatingLabel>

            {error && <Form.Text className="text-danger text-center">{error}</Form.Text>}
            <Button variant="primary" type="submit">Entrar</Button>
            <Button variant="light" onClick={() => navigate("/cadastrar")}>Cadastrar</Button>
            
        </Form>
    )
}
