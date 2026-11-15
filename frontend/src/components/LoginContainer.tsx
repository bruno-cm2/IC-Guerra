import { useState, type SubmitEvent } from "react";
import { Button, FloatingLabel, Form, FormControl } from "react-bootstrap";
import type { LoginSchema } from "../types";
import { loginAPI } from "../services/auth";
import axios from "axios";

type Props = {
    header: string
    label?: string
    onSuccess?: () => void
    className?: string
}

export const LoginContainer = ({header, label = "Usuário", onSuccess}: Props) => {

    const [error, setError] = useState<string>()

    const handleSubmit = async (event: SubmitEvent<HTMLFormElement>) => {
        event.preventDefault()

        const dados = new FormData(event.currentTarget)
        const login = Object.fromEntries(dados) as LoginSchema

        try{
            await loginAPI(login)
            onSuccess?.()
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
        <Form className="d-flex flex-column border rounded-4 shadow p-5 pt-4 gap-4 col-4"
        onSubmit={handleSubmit}>

            <h2 className="text-dark m-0">{header}</h2>

            <FloatingLabel label={label}>
                <FormControl name="login" placeholder={label} required />
            </FloatingLabel>

            <FloatingLabel label="Senha">
                <FormControl name="senha" type="password" placeholder="Senha" required />
            </FloatingLabel>

            {error && <Form.Text className="text-danger text-center">{error}</Form.Text>}
            <Button variant="primary" type="submit">Entrar</Button>
            
        </Form>
    )
}
