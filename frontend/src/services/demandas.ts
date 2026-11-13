import type { DemandaSchema } from "../types";
import { api } from "./api";


export const getDemanda = (tipo: string, periodo: number) => api.get<DemandaSchema>('demandas', {params: {tipo, periodo}})