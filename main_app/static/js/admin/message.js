const messagesDiv = document.getElementById("messages")

function addMessage(message){
    const messageEl = document.createElement("h4")
    messageEl.textContent = message
    messagesDiv.appendChild(messageEl)
}