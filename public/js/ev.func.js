function obtenerNombreMes(numeroMes) {
    const meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];
    // Ajusta el índice porque los meses generalmente van del 1 al 12
    if (numeroMes < 1 || numeroMes > 12) return null;
    return meses[numeroMes - 1];
}

function obtenerMesesAlPeriodo(periodo) {
    const meses = [];
    for (let i = 1; i <= periodo; i++) {
        meses.push(obtenerNombreMes(i));
    }
    return meses;
}

function formatNumber(number) {
    const mxn = new Intl.NumberFormat('ex-MX', {
        style: 'decimal'
    })

    return mxn.format(number)
}