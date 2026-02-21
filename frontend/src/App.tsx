import { useState } from 'react'
import './App.css'
import Ex1 from './pages/Ex1/Ex1'
import Ex2 from './pages/Ex2/Ex2'
import Ex3 from './pages/Ex3/Ex3'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Ex1/>
      <Ex2/>
      <Ex3/>
    </>
  )
}

export default App
