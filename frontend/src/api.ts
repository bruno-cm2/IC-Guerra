import axios, { type AxiosInstance } from 'axios'
import type { Demanda } from './types'

export const api: AxiosInstance = axios.create({
    baseURL: '/api/'
})

export const TIPOS: string[] = (await api.get<string[]>('demandas')).data
export const getDemanda = (tipo: string, periodo: number) => api.get<Demanda>('demandas', {params: {tipo, periodo}})