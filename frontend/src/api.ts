import axios, { type AxiosInstance } from 'axios'
import type { Demanda } from './types'

export const api: AxiosInstance = axios.create({baseURL: "http://localhost:8000"})
export const getDemanda = (tipo: string, periodo: number) => api.get<Demanda>('demandas', {params: {tipo, periodo}})