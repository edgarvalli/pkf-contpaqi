const app = Vue.createApp({
    delimiters: ['({', '})'],
    data() {
        return {
            categorias: [],
            data: {},
            nombreEmpresa: "",
            meses: [],
            periodos: 0,
            ejercicio: 0,
            loadingModal: null,
            loadingModalText: 'Cargando Balance General',
            secciones: 0,
            fullTable: false
        }
    },
    mounted() {
        this.nombreEmpresa = window.sessionStorage.getItem("empresa") || "No hay empresa";
        const now = new Date()

        this.ejercicio = now.getFullYear()
        this.periodos = now.getMonth() + 1

        this.generarBalanceGeneral()
    },
    methods: {
        reloadPage(){
            this.generarBalanceGeneral()
        },
        async generarBalanceGeneral() {
            document.getElementById('modal-button').click()
            let dbname = window.sessionStorage.getItem("dbname")
            if (dbname === null) return alert("No hay empresa seleccionada");
            this.obtenerMesesAlPeriodo()
            const request = await fetch(`/api/${dbname}/balanceGeneral/${this.ejercicio}?periodos=${this.periodos}`)
            if (!request.ok) {
                this.loadingModalText = "Error al obtener las categorías contables"
                throw new Error("Error al obtener las categorías contables");
            }

            const response = await request.json()

            if (response.error) return this.loadingModalText = response.message;
            this.data = response.data
            this.categorias = Object.keys(this.data)
            setTimeout(() => document.getElementById('modal-button-close').click(), 500)
        },
        obtenerMesesAlPeriodo() {
            const meses = [];
            for (let i = 1; i <= this.periodos; i++) {
                meses.push(obtenerNombreMes(i));
            }
            this.meses = meses;
            return meses;
        },
        formatNumber(number) {
            const mxn = new Intl.NumberFormat('ex-MX', {
                style: 'decimal'
            })

            return mxn.format(Math.ceil(number))
        },
        cambiarLayout(el) {
            if(this.fullTable) {
                this.fullTable = false;
                el.target.classList.remove('bi-grid-1x2')
                el.target.classList.add('bi-list')
            } else {
                this.fullTable = true;
                el.target.classList.remove('bi-list')
                el.target.classList.add('bi-grid-1x2')
            }
        }
    }
})

app.mount("#app")