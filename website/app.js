async function getCustomerDetails() { 
const customerId =
    document.getElementById("customerId").value.trim();

const token =
    document.getElementById("token").value.trim();

const resultDiv =
    document.getElementById("result");

resultDiv.innerHTML = "";

if (!customerId) {

    resultDiv.className = "error";

    resultDiv.innerHTML =
        "Please enter Customer ID";

    return;
}

if (!token) {

    resultDiv.className = "error";

    resultDiv.innerHTML =
        "Please enter Auth Token";

    return;
}

try {

    // Replace after deployment
    const apiUrl =
        "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/details";

    const response = await fetch(apiUrl, {

        method: "GET",

        headers: {
            "customer_id": customerId,
            "auth-token": token,
            "Content-Type": "application/json"
        }
    });

    const data = await response.json();

    if (response.ok){

         resultDiv.className = "success";

         resultDiv.innerHTML = `
             <h3>Customer Details</h3>
             <p><strong>Customer ID:</strong> ${data.customer_id}</p>
             <p><strong>Transaction Count:</strong> ${data.transaction_count}</p>
             <p><strong>Total Amount:</strong> ₹${data.total_amount}</p>
    };
     else {

        resultDiv.className = "error";

        resultDiv.innerHTML =
            data.message || "Failed to fetch data";
    }
} catch (error) {

    console.error(error);

    resultDiv.className = "error";

    resultDiv.innerHTML =
        "Error connecting to API Gateway.";
    }}
