document.getElementById('prediction-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const featuresInput = document.getElementById('features').value;
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    
    const resultContainer = document.getElementById('result-container');
    const errorContainer = document.getElementById('error-container');
    const predictionResult = document.getElementById('prediction-result');
    const predictionMessage = document.getElementById('prediction-message');
    const errorMessage = document.getElementById('error-message');

    // UI Loading state
    btnText.classList.add('hidden');
    loader.classList.remove('hidden');
    submitBtn.disabled = true;
    resultContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
    resultContainer.classList.remove('mine');

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ features: featuresInput }),
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            predictionResult.textContent = data.prediction;
            predictionMessage.textContent = data.message;
            
            if (data.prediction.toLowerCase() === 'mine') {
                resultContainer.classList.add('mine');
            }
            
            resultContainer.classList.remove('hidden');
        } else {
            // Error from server
            errorMessage.textContent = data.error || 'An unknown error occurred.';
            errorContainer.classList.remove('hidden');
        }
    } catch (error) {
        // Network or parsing error
        errorMessage.textContent = 'Failed to connect to the server. Make sure it is running.';
        errorContainer.classList.remove('hidden');
    } finally {
        // Restore UI state
        btnText.classList.remove('hidden');
        loader.classList.add('hidden');
        submitBtn.disabled = false;
    }
});
