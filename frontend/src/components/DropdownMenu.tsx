import { Dropdown } from "react-bootstrap"
import { useState } from "react"

interface Props{
    opcoes: string[] | number[]
    className?: string
    placeholder?: string
    variant?: string
    onChange?: (valor: string) => void
}

export const DropdownMenu = ({opcoes, className, placeholder, variant, onChange}: Props) => {
    const [opcao, setOpcao] = useState<string | number |null>(placeholder || opcoes[0])

    const handleSelect = (eventKey: string | null) =>{
        if (eventKey == null) return
        setOpcao(eventKey)
        onChange?.(eventKey)
    }

    return (
        <Dropdown className={className} onSelect={handleSelect}>
            <Dropdown.Toggle variant={variant}>
                {opcao}
            </Dropdown.Toggle>
            <Dropdown.Menu>
                {opcoes.map(o => <Dropdown.Item key={o} eventKey={o}>{o}</Dropdown.Item>)}
            </Dropdown.Menu>
        </Dropdown>
    )
}