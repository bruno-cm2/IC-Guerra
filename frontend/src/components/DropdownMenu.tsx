import { Dropdown, Placeholder } from "react-bootstrap"
import { useState } from "react"

interface Props{
    opcoes: string[]
}

export const DropdownMenu = ({opcoes}: Props, placeholder: string = "Escolha") => {
    const [opcao, setOpcao] = useState<string | null>(placeholder)

    return (
        <Dropdown onSelect={eventKey => setOpcao(eventKey)}>
            <Dropdown.Toggle variant="primary">
                {opcao}
            </Dropdown.Toggle>
            <Dropdown.Menu>
                {opcoes.map(o => <Dropdown.Item key={o} eventKey={o}>{o}</Dropdown.Item>)}
            </Dropdown.Menu>
        </Dropdown>
    )
}