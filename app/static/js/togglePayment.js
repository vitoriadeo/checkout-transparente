
function togglePayment(method) {
    document.getElementById('payment-card').style.display = 'none';
    document.getElementById('payment-pix').style.display = 'none';
    document.getElementById('payment-boleto').style.display = 'none';

    document.getElementById('lbl-card').classList.remove('selected');
    document.getElementById('lbl-pix').classList.remove('selected');
    document.getElementById('lbl-boleto').classList.remove('selected');

    document.getElementById('payment-' + method).style.display = 'block';
    document.getElementById('lbl-' + method).classList.add('selected');
}
