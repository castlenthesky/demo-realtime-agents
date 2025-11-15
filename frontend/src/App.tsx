import { A } from '@solidjs/router'
import { useSocketStatus } from './context/socket-provider'
import './App.css'

function App(props: { children?: any }) {
  const { connected, socketId } = useSocketStatus()

  return (
    <>
      <header>
        <nav>
          <div class="nav-links">
            <A href="/" end>Home</A>
            <A href="/about">About</A>
          </div>
          <div class="socket-status">
            <div class="status-row">
              <div class={`status-indicator ${connected() ? 'connected' : 'disconnected'}`} />
              <span class="status-text">
                {connected() ? 'Connected' : 'Disconnected'}
              </span>
            </div>
            {socketId() && (
              <span class="socket-id">ID: {socketId()}</span>
            )}
          </div>
        </nav>
      </header>
      <main>
        {props.children}
      </main>
    </>
  )
}

export default App
