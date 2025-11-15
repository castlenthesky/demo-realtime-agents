/* @refresh reload */
import { Route, Router } from '@solidjs/router'
import { render } from 'solid-js/web'
import App from './App.tsx'
import { SocketProvider } from './context/socket'
import './index.css'
import Home from './pages/Home'
import Ping from './pages/Ping'

const root = document.getElementById('root')

render(() => (
  <SocketProvider>
    <Router root={App}>
      <Route path="/" component={Home} />
      <Route path="/ping" component={Ping} />
    </Router>
  </SocketProvider>
), root!)
