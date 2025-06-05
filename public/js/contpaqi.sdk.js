
const contpaqiSDK = {
    endpoint: "/api",
    contabilidad(dbname = "") {
        const makeUrl = (path) => {
            return `${this.endpoint}/contabilidad/${path}`;
        }
        return {
            listaEmpresas: async () => {
                const request = await fetch(makeUrl("empresas"));
                if (!request.ok) {
                    throw new Error("Error al obtener la lista de empresas");
                }
                const response = await request.json();
                return response;
            },
            analisisBalanceGeneral: async (ejercicio) => {
                const request = await fetch(makeUrl(`${dbname}/analisisBalanceGeneral/${ejercicio}`));
                if (!request.ok) {
                    throw new Error("Error al obtener el análisis de balance general");
                }
                const response = await request.json();
                return response;
            },
            balanceGeneral: async (ejercicio, periodos = 12) => {
                const request = await fetch(makeUrl(`${dbname}/balanceGeneral/${ejercicio}?periodos=${periodos}`));
                if (!request.ok) {
                    throw new Error("Error al obtener el balance general");
                }
                const response = await request.json();
                return response;
            }
        }
    }
}