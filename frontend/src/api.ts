import axios, { type AxiosInstance } from 'axios'
import type { Demanda } from './types'

export const api: AxiosInstance = axios.create({
    baseURL: 'http://localhost:8000/'
})

export const TIPOS: string[] = (await api.get<string[]>('demandas/tipos')).data
export const getDemanda = (tipo: string) => api.get<Demanda>('demanda/' + tipo)