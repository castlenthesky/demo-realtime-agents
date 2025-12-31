/* @refresh reload */
import { Route, Router } from '@solidjs/router'
import { render } from 'solid-js/web'
import App from './App.tsx'
import { SocketProvider } from './context/socket'
import './index.css'
import Facts from './pages/Facts'
import Home from './pages/Home'
import Ping from './pages/Ping'
import Sandbox from './pages/Sandbox'
import TicTacToe from './pages/TicTacToe'

const root = document.getElementById('root')

render(() => (
  <SocketProvider>
    <Router root={App}>
      <Route path="/" component={Home} />
      <Route path="/facts" component={Facts} />
      <Route path="/ping" component={Ping} />
      <Route path="/tic-tac-toe" component={TicTacToe} />
      <Route path="/sandbox" component={Sandbox} />
    </Router>
  </SocketProvider>
), root!)
