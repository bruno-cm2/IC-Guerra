import { Container } from "react-bootstrap";
import { LoginContainer } from "../components/LoginContainer";

export const Login = () => {
    return(
        <Container fluid className="d-flex p-3 justify-content-evenly align-items-center min-vh-100">
            <LoginContainer header="Moderador" label = "E-mail"/>
            <LoginContainer header="Equipe" label = "Nome da equipe"/>
        </Container>
    )
}