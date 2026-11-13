import { BrowserRouter, Navigate, Route, Routes } from "react-router"
import { Grafico } from "../pages/grafico"
import { Cadastro } from "../pages/cadastro";
import { Login } from "../pages/login";

export const Rotas = () => {
  return(
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/cadastrar" Component={Cadastro}></Route>
        <Route path="/login" Component={Login}></Route>
        <Route path="/home" Component={Grafico}></Route>
      </Routes>
    </BrowserRouter>
  )
}