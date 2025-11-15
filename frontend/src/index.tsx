/* @refresh reload */
import { render } from 'solid-js/web'
import { Router, Route } from '@solidjs/router'
import './index.css'
import App from './App.tsx'
import Home from './pages/Home'
import About from './pages/About'

const root = document.getElementById('root')

render(() => (
  <Router root={App}>
    <Route path="/" component={Home} />
    <Route path="/about" component={About} />
  </Router>
), root!)
