import { DropdownMenu } from "./components/DropdownMenu"
import { TIPOS } from "./api"

export const App = () => {

  return (
    <DropdownMenu opcoes = {TIPOS}></DropdownMenu>
  )
}
