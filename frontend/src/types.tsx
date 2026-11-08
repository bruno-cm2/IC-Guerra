interface components {
  schemas: {
    DemandaModel: {
      tipo: string;
      minimo: number;
      maximo: number;
      n_periodos: number;
      dados: number[];
      amplitude: number;
      referencias?: number[] | null;
    };
  };
}

export type Demanda = components["schemas"]["DemandaModel"]