const API_KEY = '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'
const submitButton = document.querySelector('#submit')
const outputElement = document.querySelector('#output')
const inputElement = document.querySelector('input')
const historyElement = document.querySelector('.history')
const buttonElement = document.querySelector('button')

function changeInput(value) {
	const inputElement = document.querySelector('input')
	inputElement.value = value
}

async function getMessage() {
	console.log('clicked!')
	const options = {
		method: 'POST',
		headers: {
			'Authorization': 'Bearer ' + API_KEY,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			model: 'gpt-3.5-turbo',
			messages: [{ role: 'user', content: inputElement.value }]
		})
	}
	try {
		// const input = inputElement.value 
		// outputElement.textContent = inputElement.value
		// inputElement.value = ''
		// outputElement.textContent = 'Please wait while we generate your response...'

		const response = await fetch('https://api.openai.com/v1/chat/completions', options)
		const data = await response.json()
		console.log(data)

		outputElement.textContent = data.choices[0].message.content

		if (data.choices[0].message.content) {
			const pElement = document.createElement('p')
			pElement.textContent = data.choices[0].message.content 
			pElement.addEventListener('click', () => changeInput(pElement.textContent))
			historyElement.append(pElement)
			
		}
	}
	catch (error) {
		console.log(error)
	}
}

submitButton.addEventListener('click', getMessage)

function clearInput() {
	inputElement.value = ''
}

submitButton.addEventListener('click', clearInput)
