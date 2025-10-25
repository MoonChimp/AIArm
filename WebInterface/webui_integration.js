// Function to generate images using StableDiffusionWebUI API
async function generateImageWithWebUI(prompt) {
    try {
        // WebUI default port is 7860, but let's make it configurable
        const webUIPort = localStorage.getItem('sd_webui_port') || '7860';
        const webUIUrl = `http://localhost:${webUIPort}/sdapi/v1/txt2img`;
        
        // Default parameters (user can customize these in a settings panel)
        const params = {
            prompt: prompt,
            negative_prompt: "blurry, bad anatomy, extra limbs, poorly drawn face, distorted face",
            steps: 25,
            width: 512,
            height: 512,
            cfg_scale: 7.5,
            sampler_name: "DPM++ 2M Karras"
        };
        
        console.log(`Generating image with StableDiffusionWebUI: ${prompt}`);
        
        // Make the API call
        const response = await fetch(webUIUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        
        if (response.ok) {
            const data = await response.json();
            
            // WebUI returns images as base64
            if (data.images && data.images.length > 0) {
                return {
                    success: true,
                    image: `data:image/jpeg;base64,${data.images[0]}`
                };
            }
        } else {
            throw new Error(`API returned status: ${response.status}`);
        }
        
        return { success: false };
    } catch (error) {
        console.error('Error generating image with WebUI:', error);
        return { success: false, error: error.toString() };
    }
}

// Function to check if WebUI is available
async function checkWebUIAvailability() {
    try {
        // Get port from local storage or use default
        const webUIPort = localStorage.getItem('sd_webui_port') || '7860';
        
        // Try to connect to WebUI
        const response = await fetch(`http://localhost:${webUIPort}/sdapi/v1/sd-models`, {
            method: 'GET'
        });
        
        if (response.ok) {
            const models = await response.json();
            console.log(`WebUI is available with ${models.length} models`);
            return true;
        }
        
        return false;
    } catch (error) {
        console.error('Error checking WebUI availability:', error);
        return false;
    }
}

// Update the processUserInput function to try WebUI first
async function processUserInput() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Clear input
    userInput.value = '';
    
    // Add user message to UI
    addMessageToUI(message, true);
    
    // Add to chat history
    chatHistory.push({ role: "user", content: message });
    
    // Check if this is a photo generation request
    const isPhotoRequest = message.toLowerCase().includes('photo') || 
                         message.toLowerCase().includes('picture') || 
                         message.toLowerCase().includes('image') || 
                         message.toLowerCase().includes('generate') || 
                         message.toLowerCase().includes('create');
                         
    // Show typing indicator
    typingIndicator.style.display = 'block';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // If it's a photo request, try to generate an image first
    if (isPhotoRequest) {
        try {
            // First check if WebUI is available
            const hasWebUI = await checkWebUIAvailability();
            
            if (hasWebUI) {
                // Try to generate with WebUI
                const imageResult = await generateImageWithWebUI(message);
                if (imageResult && imageResult.success) {
                    // Hide typing indicator
                    typingIndicator.style.display = 'none';
                    
                    // Add image to UI
                    addImageToUI(imageResult.image, message);
                    
                    // Add assistant response to chat history
                    const imageResponse = `Photo Generation Agent: I've created this image based on your request: "${message}"`;
                    chatHistory.push({ role: "assistant", content: imageResponse });
                    return;
                }
            }
            
            // If WebUI failed, fall back to Ollama
            const hasImageModel = await checkImageGenerationModel();
            
            if (hasImageModel) {
                // Try to generate an image
                const imageResult = await generateImage(message);
                if (imageResult && imageResult.success) {
                    // Hide typing indicator
                    typingIndicator.style.display = 'none';
                    
                    // Add image to UI
                    addImageToUI(imageResult.image, message);
                    
                    // Add assistant response to chat history
                    const imageResponse = `Photo Generation Agent: I've created this image based on your request: "${message}"`;
                    chatHistory.push({ role: "assistant", content: imageResponse });
                    return;
                }
            }
        } catch (error) {
            console.error('Error generating image:', error);
        }
    }
    
    // If we get here, either it wasn't an image request or image generation failed
    // Proceed with normal text response
    const response = await sendMessageToOllama(message);
    
    // Hide typing indicator
    typingIndicator.style.display = 'none';
    
    // Add assistant response to UI
    addMessageToUI(response);
    
    // Add to chat history
    chatHistory.push({ role: "assistant", content: response });
}
