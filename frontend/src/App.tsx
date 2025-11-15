import { A } from '@solidjs/router'
import './App.css'
import { useSocketStatus } from './context/socket'

function App(props: { children?: any }) {
  const { connected, socketId } = useSocketStatus()

  return (
    <>
      <header>
        <nav>
          <div class="nav-links">
            <A href="/" end>Home</A>
            <A href="/ping">Ping</A>
            <A href="/tic-tac-toe">Tic Tac Toe</A>
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
