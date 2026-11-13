import { type SubmitEvent } from "react";
import { Button, FloatingLabel, Form, FormControl } from "react-bootstrap";

export const Cadastro = () => {

    const handleSubmit = (event: SubmitEvent<HTMLFormElement>) => {
        event.preventDefault()
    }
    
    return(
        <Form className="w-50 d-flex flex-column border rounded-5 shadow m-auto p-5 pt-4 gap-4" onSubmit={handleSubmit}>
            <h1 className="text-dark m-0">Crie sua conta</h1>
            <FloatingLabel controlId="nome" label="Nome">
                <FormControl placeholder="Nome" required />
            </FloatingLabel>

            <FloatingLabel controlId="email" label="E-mail">
                <FormControl type="email" placeholder="E-mail" required />
            </FloatingLabel>

            <FloatingLabel controlId="senha" label="Senha">
                <FormControl type="password" placeholder="Senha" required />
            </FloatingLabel>
            <Button variant="primary" type="submit">Criar</Button>
        </Form>
    )
}
