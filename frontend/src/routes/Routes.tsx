import { BrowserRouter, Route, Routes } from "react-router-dom"
import { Grafico } from "../pages/grafico"

export const Rotas = () => {
  return(
    <BrowserRouter>
      <Routes>
        <Route path="/" Component={() => <Grafico/>}></Route>
      </Routes>
    </BrowserRouter>
  )
}