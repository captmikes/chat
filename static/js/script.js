let threadId = null;

function startConversation() {
    fetch('/start')
    .then(response => response.json())
    .then(data => {
        threadId = data.thread_id;
    })
    .catch(error => console.error('Error starting conversation:', error));
}

document.addEventListener('DOMContentLoaded', startConversation);

document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== '') {
        document.getElementById('send-btn').disabled = true;
        updateChat(userInput, true);
        document.getElementById('responding-indicator').style.display = 'block';
        sendMessage(userInput);
        document.getElementById('user-input').value = '';
    }
});

function sendMessage(message) {
    if (threadId === null) {
        console.error('No thread ID found. Cannot send message.');
        return;
    }

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message, thread_id: threadId }),
    })
    .then(response => response.json())
    .then(data => {
        updateChat(data.response);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function updateChat(message, isSender = false) {
    document.getElementById('responding-indicator').style.display = 'none';
    document.getElementById('send-btn').disabled = false;
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    messageElement.textContent = message;
    messageElement.classList.add('chat-bubble');

    if (isSender) {
        messageElement.classList.add('sender');
    } else {
        messageElement.classList.add('receiver');
    }

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Enable sending messages with Enter key
document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('send-btn').click();
    }
});

