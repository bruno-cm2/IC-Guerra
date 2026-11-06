import { TIPOS } from "../api"
import { DropdownMenu } from "../components/DropdownMenu"

export const Grafico = (tipo: string) => {
    return(
        <DropdownMenu opcoes={TIPOS}></DropdownMenu>
    )
} 