const btnResultado = document.querySelector('#btn-resultado');
const btnOriginal = document.querySelector('#btn-original');
const imgResultado = document.querySelector('#img-resultado');
const imgOriginal = document.querySelector('#img-original');

imgResultado.style.display = 'block';

btnResultado.addEventListener("change", () => {
    if (btnResultado.checked) {
        imgResultado.style.display = 'block';
        imgOriginal.style.display = 'none';
    }
});

btnOriginal.addEventListener("change", () => {
    if (btnOriginal.checked) {
        imgOriginal.style.display = 'block';
        imgResultado.style.display = 'none';
    }
});
