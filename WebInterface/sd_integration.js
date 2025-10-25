// StableDiffusionWebUI Integration 
 
// Configuration 
const WEBUI_PORT = 7860; 
const WEBUI_URL = `http://localhost:${WEBUI_PORT}`; 
 
// Generate image using WebUI 
async function generateWithWebUI(prompt) { 
  try { 
    console.log(`Generating image via WebUI: ${prompt}`); 
    const response = await fetch(`${WEBUI_URL}/sdapi/v1/txt2img`, { 
      method: 'POST', 
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify({ 
        prompt: prompt, 
        negative_prompt: "blurry, bad anatomy, extra limbs, poorly drawn face", 
        steps: 25, 
        width: 512, 
        height: 512 
      }) 
    }); 
 
    if (!response.ok) throw new Error(`WebUI returned ${response.status}`); 
    const data = await response.json(); 
 
      return { success: true, image: `data:image/jpeg;base64,${data.images[0]}` }; 
    } 
 
    return { success: false, error: "No image returned" }; 
  } catch (error) { 
    console.error("WebUI error:", error); 
    return { success: false, error: error.toString() }; 
  } 
} 
 
// Check WebUI availability 
async function checkWebUI() { 
  try { 
    const response = await fetch(`${WEBUI_URL}/sdapi/v1/sd-models`); 
    return response.ok; 
  } catch (error) { 
    return false; 
  } 
} 
 
// Override the image generation in processUserInput 
document.addEventListener('DOMContentLoaded', function() { 
  // Store original function 
  const originalProcessUserInput = window.processUserInput; 
 
  // Check WebUI availability and update status 
  checkWebUI().then(available =
    if (available) { 
      const statusEl = document.getElementById('status-text'); 
      if (statusEl) statusEl.innerHTML += ' + WebUI'; 
      console.log('WebUI available!'); 
    } 
  }); 
 
  // Replace the function 
  window.processUserInput = async function() { 
    const message = userInput.value.trim(); 
    if (!message) return; 
 
    // Clear input and display user message 
    userInput.value = ''; 
    addMessageToUI(message, true); 
    chatHistory.push({ role: "user", content: message }); 
 
    // Check if image request 
    const imageKeywords = ['image', 'picture', 'photo', 'generate', 'create', 'draw']; 
    const isImageRequest = imageKeywords.some(kw =
 
    // Show typing indicator 
    typingIndicator.style.display = 'block'; 
    messagesContainer.scrollTop = messagesContainer.scrollHeight; 
 
    if (isImageRequest) { 
      try { 
        // Check WebUI availability 
        const webUIAvailable = await checkWebUI(); 
 
        if (webUIAvailable) { 
          // Generate image 
          const result = await generateWithWebUI(message); 
 
          if (result.success) { 
            // Hide typing indicator 
            typingIndicator.style.display = 'none'; 
 
            // Create image element 
            const messageElement = document.createElement('div'); 
            messageElement.classList.add('message', 'assistant-message'); 
 
            // Badge 
            const badge = document.createElement('div'); 
            badge.classList.add('agent-badge', 'agent-photo'); 
            badge.textContent = '📷 Photo Generation Agent'; 
            messageElement.appendChild(badge); 
 
            // Image 
            const img = document.createElement('img'); 
            img.src = result.image; 
            img.alt = message; 
            img.style.maxWidth = '100%'; 
            img.style.borderRadius = '8px'; 
            img.style.marginTop = '10px'; 
            messageElement.appendChild(img); 
 
            // Caption 
            const caption = document.createElement('div'); 
            caption.textContent = `Here's the image you requested.`; 
            caption.style.marginTop = '8px'; 
            messageElement.appendChild(caption); 
 
            // Add to chat 
            messagesContainer.appendChild(messageElement); 
            messagesContainer.scrollTop = messagesContainer.scrollHeight; 
 
            // Add to chat history 
            chatHistory.push({ role: "assistant", content: "Photo Generation Agent: I've created an image based on your request." }); 
            return; 
          } 
        } 
      } catch (error) { 
        console.error('WebUI integration error:', error); 
      } 
    } 
 
    // Fall back to original method 
    return originalProcessUserInput.call(this); 
  }; 
}); 
