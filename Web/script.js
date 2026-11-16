const selector = document.getElementById("destino-mapa");
const mapa = document.getElementById("mapa-google");

selector.addEventListener("change", function () {

    const destino = selector.value;

    const ubicacion = encodeURIComponent(destino);

    mapa.src = `https://www.google.com/maps?q=${ubicacion}&output=embed`;

});