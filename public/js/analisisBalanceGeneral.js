const app = Vue.createApp({
    delimiters: ['({', '})'],
    data() {
        return {
            cuentasMayor: [],
            cuentas: {},
            meses: [],
            periodo: 0,
            ejercicio: 0,
            modalButton: document.getElementById('modal-button')
        }
    },
    mounted() {
        this.nombreEmpresa = window.sessionStorage.getItem("empresa") || "No hay empresa";
        const now = new Date()

        this.ejercicio = now.getFullYear()
        this.periodo = now.getMonth() + 1;
        this.correrAnalisis()
    },
    methods: {
        async correrAnalisis() {
            // this.loadingModal.show()
            document.getElementById('modal-button').click()
            let dbname = window.sessionStorage.getItem("dbname")
            if (dbname === null) return alert("No hay empresa seleccionada");
            this.meses = obtenerMesesAlPeriodo(this.periodo)
            const request = await fetch(`/api/${dbname}/analisisBalanceGeneral/${this.ejercicio}`)
            if (!request.ok) {
                this.loadingModalText = "Error al obtener el analisis"
                throw new Error("Error al obtener el analisis");
            }

            const response = await request.json()

            if (response.error) return this.loadingModalText = response.message;
            this.cuentas = response.data
            setTimeout(() => document.getElementById('modal-button-close').click(), 500)
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