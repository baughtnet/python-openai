const App = () => {
  const getMessages = async () => {
    const options = {
      method: "POST",
      body : JSON.stringify({
        messages: "hello, how are you?" 
      }),
      headers: {
        "Content-Type": "application/json"
      }
    }
    try {
      const response = await fetch('http://localhost:3100/completions', options) 
      const data = response.json()
      console.log(data)
    } catch (error) {
      console.log(error)
    }
  }
  return (
    <div className="app">
    <section className="side-bar">
      <button>+ New Chat</button>
      <ul className="history">
      <li>test</li> 
      </ul>
      <nav>
        <p>@baughtnet</p>
      </nav>
    </section>
    <section className="main">
        <h1>ChatGPT</h1>
        <ul className="feed">

        </ul>
        <div className="bottom-section">
          <div className="input-container">
            <input/>
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
