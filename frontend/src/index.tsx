/* @refresh reload */
import { render } from 'solid-js/web'
import { Router, Route } from '@solidjs/router'
import './index.css'
import App from './App.tsx'
import Home from './pages/Home'
import About from './pages/About'
import { SocketProvider } from './context/socket-provider.tsx'

const root = document.getElementById('root')

render(() => (
  <SocketProvider>
    <Router root={App}>
      <Route path="/" component={Home} />
      <Route path="/about" component={About} />
    </Router>
  </SocketProvider>
), root!)
