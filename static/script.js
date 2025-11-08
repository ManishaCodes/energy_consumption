async function sendPrediction() {
  const inputField = document.getElementById("inputData");
  const resultDiv = document.getElementById("result");

  // Clean and parse user input
  const rawValues = inputField.value.trim().split(",").map(v => parseFloat(v));

  if (rawValues.length !== 36 || rawValues.some(isNaN)) {
    resultDiv.innerHTML = "⚠️ Please enter exactly 36 valid numeric values!";
    resultDiv.style.color = "red";
    return;
  }

  const payload = { input: [[rawValues]] };

  try {
    resultDiv.innerHTML = "⏳ Predicting... please wait.";
    resultDiv.style.color = "#333";

    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);

    const data = await response.json();
    console.log("Response from Flask:", data); // debug line

    if (data.status === "success") {
      resultDiv.innerHTML = `✅ Predicted Energy Load: <strong>${data.predicted_load.toFixed(4)}</strong>`;
      resultDiv.style.color = "#0078ff";
    } else {
      resultDiv.innerHTML = `❌ Error: ${data.message}`;
      resultDiv.style.color = "red";
    }
  } catch (error) {
    console.error("Error sending request:", error);
    resultDiv.innerHTML = "⚠️ Could not connect to backend. Make sure Flask is running.";
    resultDiv.style.color = "red";
  }
}

// Load Sample Button
function loadSample() {
  const sampleValues = [
    447,329,0,4844,4821,162,0,0,0,863,1051,1899,0,7096,43,73,49,196,
    0,6378,17,6436,26118,25385,50.1,65.41,6.19,75.06,0.081,0.063,0.098,
    29197.97,18026.74,19252.04,23,2
  ];
  document.getElementById("inputData").value = sampleValues.join(",");
  document.getElementById("result").innerHTML = "✅ Sample data loaded!";
  document.getElementById("result").style.color = "#28a745";
}
