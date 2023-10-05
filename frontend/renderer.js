const electron = require('electron')
const ipc = electron.ipcRenderer
const axios = require('axios');

const chatbot = document.getElementById('chatbot');
const conversation = document.getElementById('conversation');
const inputForm = document.getElementById('input-form');
const inputField = document.getElementById('input-field')

// Add event listener to input form
inputForm.addEventListener('submit', async function(event) {
    // Prevent form submission
    event.preventDefault();
  
    // Get user input
    const input = inputField.value;
  
    // Clear input field
    inputField.value = '';
    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: "2-digit" });
  
    // Add user input to conversation
    let message = document.createElement('div');
    message.classList.add('chatbot-message', 'user-message');
    message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${input}</p>`;
    conversation.appendChild(message);
  
    // Generate chatbot response
    const response = await generateResponse(input);
    console.log("Chatbot response:", response)
  
    // Add chatbot response to conversation
    message = document.createElement('div');
    message.classList.add('chatbot-message','chatbot');
    message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${response}</p>`;
    conversation.appendChild(message);
    message.scrollIntoView({behavior: "smooth"});
  });

function sendToPython() {
    var { PythonShell } = require('python-shell');
    const path = require('path');
    const options = {
      mode: 'text',
      args: [inputField.value],
      pythonPath: path.join(__dirname, '../../Venvs/chatbot-venv/Scripts/python.exe'),
    };
  
    PythonShell.run('../evaluation.py', options, function (err, results) {
      if (err) throw err;
      // results is an array consisting of messages collected during execution
      console.log('results: ', results);
    });
  }


async function generateResponse(input) {
    try {
        const response = await axios.get(`http://127.0.0.1:5001/${input}`)
        console.log("Response:", response.data);
        return response.data;
    } catch (error) {    
        console.log(error);
    }
    // axios.post(`http://127.0.0.1:5001/${input}`)
    // .then(function (response) {
    //  console.log("Response: ", response.data);
    // })
    // .catch(function (error) {
    //  console.log(error);
    // });
}

sendToPython();
