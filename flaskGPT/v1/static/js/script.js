const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const chatForm = document.getElementById('chat-form');

chatForm.addEventListener('submit', function(event) {
  event.preventDefault();

  // Send user input to server using AJAX
  fetch('/chat', {
    method: 'POST',
    body: JSON.stringify({ user_input: userInput.value }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    // Update chat history with server response
    chatHistory.innerHTML += `<div class="message ${data.role}">${data.content}</div>`;
    userInput.value = '';

    // Additional logic for scrolling, highlighting, etc.

  })
  .catch(error => {
    console.error(error);
  });
});

// Add event listener for enter key (optional)
userInput.addEventListener('keydown', function(event) {
  if (event.ctrlKey && event.key === 'Enter') {
    userInput.submit();
  } else if (enter.key === 'Enter') {
    event.preventDefault();
  }
});
