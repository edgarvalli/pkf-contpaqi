const app = Vue.createApp({
    delimiters: ['({', '})'],
    data() {
        return {
            cuentasMayor: [],
            cuentas: {},
            meses: [],
            periodo: 0,
            ejercicio: 0,
            loadingModalID: "loading-modal-id"
        }
    },
    mounted() {
        
        const now = new Date()

        this.ejercicio = now.getFullYear()
        this.periodo = now.getMonth() + 1;
        this.correrAnalisis();

        document.getElementById("lista-empresas-modal-id").addEventListener('hidden.bs.modal', () => {
            this.correrAnalisis();
        });

    },
    methods: {
        async correrAnalisis() {
            
            new bootstrap.Modal(document.getElementById(this.loadingModalID)).show();
            this.nombreEmpresa = window.sessionStorage.getItem("empresa") || "No hay empresa";

            let dbname = window.sessionStorage.getItem("dbname")
            if (dbname === null) return alert("No hay empresa seleccionada");
            this.meses = obtenerMesesAlPeriodo(this.periodo)
            const response = await contpaqiSDK.contabilidad(dbname).analisisBalanceGeneral(this.ejercicio);
            if (response.error) return this.loadingModalText = response.message;
            this.cuentas = response.data

            bootstrap.Modal.getInstance(document.getElementById(this.loadingModalID)).hide();

        },
        formatNumber(number) {
            const mxn = new Intl.NumberFormat('ex-MX', {
                style: 'decimal'
            })

            return mxn.format(Math.ceil(number))
        },
    }
})

app.mount('#app')