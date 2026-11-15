import { useState, type SubmitEvent } from "react";
import { Button, Container, FloatingLabel, Form, FormControl } from "react-bootstrap";
import type { UsuarioSchema } from "../types";
import { cadastrarAPI } from "../services/auth";
import axios from "axios";
import { useNavigate } from "react-router";

export const Cadastro = () => {

    const navigate = useNavigate()
    const [error, setError] = useState<string>()

    const handleSubmit = async (event: SubmitEvent<HTMLFormElement>) => {
        event.preventDefault()

        const dados = new FormData(event.currentTarget)
        const usuario = Object.fromEntries(dados) as UsuarioSchema

        try{
            await cadastrarAPI(usuario)
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
        <Container fluid className="align-items-center p-3">
            <Form className="d-flex flex-column border rounded-5 shadow m-auto p-5 pt-4 gap-4"
            onSubmit={handleSubmit}>
                <h2 className="text-dark m-0">Crie sua conta</h2>
                <FloatingLabel label="Nome">
                    <FormControl name="nome" placeholder="Nome" required />
                </FloatingLabel>
                <FloatingLabel label="E-mail">
                    <FormControl name="email" type="email" placeholder="E-mail" required />
                </FloatingLabel>

                <FloatingLabel label="Senha">
                    <FormControl name="senha" type="password" placeholder="Senha" required />
                </FloatingLabel>
                <Button variant="primary" type="submit">Cadastrar</Button>
                <Button variant="light" onClick={() => navigate("/login")}>Login</Button>
                {error && <Form.Text className="text-danger text-center">{error}</Form.Text>}
            </Form>
        </Container>
    )
}
