import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { Demanda } from "../types";
import { useMemo } from "react";

interface Props {
  demanda: Demanda
  min?: number
  max?: number
  className?: string
  width?: number | `${number}%`
}

export const Chart = ({demanda, width, min=30000, max=50000, className}: Props) => {
  
  if(!demanda) return
  
  const meses = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez",
  ]

  const dados = useMemo(() => {
    const inicio = Math.floor(Math.random() * 12)
    return demanda.dados.map((valor, i) => ({
      periodo: meses[(inicio + i) % 12],
      valor,
      }))
    }, [demanda])

  return (
    <ResponsiveContainer width={typeof width === 'number' ? `${width}%` : width ?? '100%'} aspect={2} className={className}>
      <LineChart data={dados}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={'periodo'}/>
        <YAxis domain={[min, max]} />
        <Tooltip />
        <Line type="monotone" dataKey="valor" stroke="#0d6efd" strokeWidth={2} dot animationDuration={400} />
      </LineChart>
    </ResponsiveContainer>
  )
}