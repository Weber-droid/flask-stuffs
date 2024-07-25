document.getElementById('paymentForm').addEventListener('submit', calculateTotal);

function calculateTotal(event) {
    event.preventDefault();

    const numberOfDocuments = document.getElementById('numberOfDocuments').value;
    const deliveryOption = document.querySelector('input[name="deliveryOption"]:checked').value;

    const documentCost = 10; // Fixed cost per document
    const pickupCost = 0;
    const onCampusDeliveryCost = 5;
    const offCampusDeliveryCost = 10;

    let totalCost = numberOfDocuments * documentCost;
    let paymentMessage = '';

    if (deliveryOption === 'onCampus') {
        totalCost += onCampusDeliveryCost;
        paymentMessage = 'Make payment to delivery guy upon receiving your goods.';
    } else if (deliveryOption === 'offCampus') {
        totalCost += offCampusDeliveryCost;
        paymentMessage = 'Make payment to delivery guy upon receiving your goods.';
    } else if (deliveryOption === 'pickup') {
        paymentMessage = 'Make payment to printing provider.';
    }

    document.getElementById('result').innerHTML = `<p>Total Cost: GHS${totalCost}.00</p><p>${paymentMessage}</p><p>Thank you for working with us.</p>`;
    document.getElementById('result').style.display = 'block';
}

function logout() {
    // Add your logout functionality here
    window.location.href = "/";
    alert("Logging out...");


}