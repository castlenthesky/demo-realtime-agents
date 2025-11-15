import { A } from '@solidjs/router'
import './App.css'

function App(props: { children?: any }) {
  return (
    <>
      <header>
        <nav>
          <A href="/" end>Home</A>
          <A href="/about">About</A>
        </nav>
      </header>
      <main>
        {props.children}
      </main>
    </>
  )
}

export default App
