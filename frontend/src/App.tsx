import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/general/Layout'
import LoginPage from './pages/LoginPage'
import HomePage from './pages/HomePage'
import GamePage from './pages/GamePage'

const App: React.FC = () => {
  return (
    <Layout>
      <Routes>
        <Route path='/login' element={<LoginPage />} />
        <Route path='/' element={<HomePage />} />
        <Route path='/game' element={<GamePage />} />
        <Route path='*' element={<Navigate to='/login' replace />} />
      </Routes>
    </Layout>
  )
}

export default App
