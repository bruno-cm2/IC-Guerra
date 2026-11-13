import { BrowserRouter, Route, Routes } from "react-router"
import { Grafico } from "../pages/grafico"
import { Cadastro } from "../pages/cadastro";

export const Rotas = () => {
  return(
    <BrowserRouter>
      <Routes>
        <Route path="/" Component={Cadastro}></Route>
        <Route path="/home" Component={Grafico}></Route>
      </Routes>
    </BrowserRouter>
  )
}