import { Button, Container, FormControl, FormGroup, FormLabel, InputGroup } from "react-bootstrap"
import { getDemanda, TIPOS } from "../api"
import { DropdownMenu } from "../components/DropdownMenu"
import { useState } from "react"
import { type Demanda } from "../types"
import { Chart } from "../components/Chart"
import InputGroupText from "react-bootstrap/esm/InputGroupText"

export const Grafico = () => {

    const normalize = (str : string) => str.normalize("NFD").replace(/[\u0300-\u036f]/g, '').toLowerCase()

    const [demanda, setDemanda] = useState<Demanda>()
    const [periodo, setPeriodo] = useState<number>(8)
    const [tipo, setTipo] = useState<string>(normalize(TIPOS[0]))

    const handleTipos = (eventKey: string) =>  setTipo(normalize(eventKey))
    const handlePeriodo = (eventKey: number ) => {
        const n = Number(eventKey)
        if (!eventKey || Number.isNaN(n)) return
        setPeriodo(eventKey)
    }
    const criarDemanda = () => getDemanda(tipo, periodo).then(res => setDemanda(res.data))

    return (
        <Container className="d-flex flex-column justify-content-center align-items-center min-vh-100 gap-3 ">
            <h3>Gerar Demanda</h3>
            <div className="d-flex gap-1 align-items-baseline">
                <label>Tipo:</label> 
                <DropdownMenu variant="light" opcoes={TIPOS} onChange={handleTipos}/>
                <label className="ms-2">Período:</label>
                <InputGroup>
                    <FormControl 
                        type="number"
                        min={4} 
                        max={20} 
                        defaultValue={8} 
                        style={{ width: 70 }} 
                        onChange={(e) => handlePeriodo(Number(e.target.value))}>
                        </FormControl>
                    <InputGroupText>meses</InputGroupText>
                </InputGroup>
            </div>
            <Button variant="primary" onClick={criarDemanda}>Gerar</Button>

            {demanda && <Chart demanda={demanda} width={75} />}
        </Container>
    )
} 