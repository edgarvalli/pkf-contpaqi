const balanceGeneralVueParams = {
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
            fullTable: false,
            loadingModalID: "loading-modal-id"
        }
    },
    mounted() {
        const now = new Date()

        this.ejercicio = now.getFullYear()
        this.periodos = now.getMonth() + 1

        this.generarBalanceGeneral();

        document.getElementById("lista-empresas-modal-id").addEventListener('hidden.bs.modal', () => {
            this.generarBalanceGeneral();
        });
    },
    methods: {
        reloadPage(){
            this.generarBalanceGeneral()
        },
        async generarBalanceGeneral() {

            this.nombreEmpresa = window.sessionStorage.getItem("empresa") || "No hay empresa";
            const loadingModal = document.getElementById(this.loadingModalID);

            new bootstrap.Modal(loadingModal).show();

            let dbname = window.sessionStorage.getItem("dbname");

            if (dbname === null) return alert("No hay empresa seleccionada");
            this.obtenerMesesAlPeriodo()
            const response = await contpaqiSDK.contabilidad(dbname).balanceGeneral(this.ejercicio, this.periodos);
            if (response.error) return this.loadingModalText = response.message;
            this.data = response.data
            this.categorias = Object.keys(this.data)
            
            bootstrap.Modal.getInstance(loadingModal).hide();
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
}

Vue.createApp(balanceGeneralVueParams).mount("#balance-general-app");