import { useEffect, useState } from 'react'
import type { Demanda } from './types'
import { Dropdown, Container } from 'react-bootstrap'
import './App.css'

const API_URL = 'http://localhost:8000'


function App() {

  const [listaTipos, setListaTipos] = useState<string[]>([]) 
  const [tipo, setTipo] = useState<string>('Selecione uma demanda')
  const [demanda, setDemanda] = useState<Demanda | null>(null)
  const [erro, setErro] = useState<string | null>(null)

  useEffect(() => {
    const importarTipos = async () => {
      try{
        const resposta = await fetch(`${API_URL}/demandas/tipos`)
        if (!resposta.ok) throw new Error(`Erro ${resposta.status}`);
        const dados: string[] = await resposta.json()
        setListaTipos(dados)
      }catch(e){
        setErro(e instanceof Error ? e.message : "Erro desconhecido")
      }
    }
    importarTipos()
  }, [])

  const buscarDemanda = async (tipoSelecionado: string) => {
    try{
      setErro(null)

      const resposta = await fetch(`${API_URL}/demandas/${tipoSelecionado}`)
      if(!resposta.ok)  throw new Error(`${resposta.status}`)

      const dados: Demanda = await resposta.json()
      setDemanda(dados)
    }catch(e){
      setErro(e instanceof Error ? e.message : "Erro desconhecido")
    }
  }

  const handleSelect = (eventKey: string | null) => {
    if(!eventKey) return
    setTipo(eventKey)
    buscarDemanda(eventKey)
  }

  return (
    <Container className='m-auto shadow align-self-center rounded-3 text-center d-flex flex-column p-4'>
      <Dropdown onSelect={handleSelect}>
        <Dropdown.Toggle variant="primary" id="dropdown-demanda">
          {tipo}
        </Dropdown.Toggle>

        <Dropdown.Menu>
          {listaTipos.map((t) =>
            <Dropdown.Item key={t} eventKey={t}>
              {t}
            </Dropdown.Item>
          )}
        </Dropdown.Menu>
      </Dropdown>
      {erro && <p className="text-danger mt-3">{erro}</p>}
      {demanda && <pre className="m-3">{JSON.stringify(demanda.dados.sort())}</pre>}
    </Container>        
  )
}

export default App
