import { useState, useEffect } from 'react'

const App = () => {
  // const [ value, setValue ] = useState(null)
  const [title, setTitle] = useState(null)
  const [request, setRequest] = useState(null)
  const [ message, setMessage ] = useState(null)
  const [ previousChats, setPreviousChats ] = useState([])
  const [ currentTitle, setCurrentTitle ] = useState(null)

  const createNewChat = () => {
    setMessage(null)
    setCurrentTitle(null)
    // setValue("")
    setRequest(null)
  }

  const handleClick = (uniqueTitle) => {
    setCurrentTitle(uniqueTitle)
    setMessage(null)
    // setValue("")
    setRequest(null)
  }

  const handleChange = (e) => {
    setRequest(e.target.value)
  }

  const getMessages = async () => {
    const options = {
      method: "POST",
      body : JSON.stringify({
        message: request,
      }),
      headers: {
        "Content-Type": "application/json"
      }
    }
    try {
      const response = await fetch('http://localhost:3100/completions', options) 
      const data = await response.json()

      setMessage(data.choices[0].message)
    } catch (error) {
      console.log(error)
    }
    setRequest('')
  }

useEffect(() => {
  console.log(currentTitle, request, message)
  if (!currentTitle && request && message) {
    setCurrentTitle(request)
  }
  if (currentTitle && request && message) {
    setPreviousChats((prevChats) => 
      [...prevChats,
        {
          title: currentTitle,
          role: "user",
          content: request 
        },
        {
          title: currentTitle,
          role: message.role,
          content: message.content
        },
      ])
  }
}, [message, currentTitle, request])

    console.log(previousChats)
    const currentChat = previousChats.filter(previousChat => previousChat.title === currentTitle)
    const uniqueTitles = Array.from(new Set(previousChats.map(previousChat => previousChat.title)))

  console.log(uniqueTitles)

  return (
    <div className="app">
    <section className="side-bar">
      <button onClick={createNewChat}>+ New Chat</button>
      <ul className="history">
        {uniqueTitles?.map((uniqueTitle, index) => <li key={index} onClick={() => handleClick(uniqueTitle)}>{uniqueTitle}</li>)}
      </ul>
      <nav>
        <p>@baughtnet</p>
      </nav>
    </section>
    <section className="main">
      {!currentTitle && <h1>reactGPTv2...the working one</h1>}
        <ul className="feed">
          {currentChat?.map((chatMessage, index) => <li key={index}>
            <p className="role">{chatMessage.role}</p>
            <p className="content">{chatMessage.content}</p>
          </li>)}
        </ul>
        <div className="bottom-section">
          <div className="input-container">
            <input value={request}  onChange={handleChange}/>
            <div id="submit" onClick={getMessages}>&#x27A2;</div>
        </div>
        <p className="info">
          ChatGPT by OpenAI.  Free research preview.
          providided by @baughtnet
        </p>
    </div>
    </section>
    </div>
  )
}

export default App;
