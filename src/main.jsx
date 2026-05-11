import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'
import './styles.css'

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { seedLocalStorage } from './componentes/Datos.jsx'
seedLocalStorage()

import Inicio from './paginas/Inicio.jsx'
import Header from './componentes/Header.jsx'
import Footer from './componentes/Footer.jsx'
import Nosotros from './paginas/Nosotros.jsx'
import Centros from './paginas/Centros.jsx'
import Donacion from './paginas/Donacion.jsx'
import Necesidades from './paginas/Necesidades.jsx'
import Registro from './paginas/Registro.jsx'
import BackOffice from './paginas/BackOffice.jsx'
import Transparencia from './paginas/Transparencia.jsx'
import Importante from './assets/Importante.jsx'
import Login from './paginas/Login.jsx'
import Perfil from './paginas/Perfil.jsx'

import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom'
import { AuthProvider } from './componentes/AuthContext.jsx'
import ProtectedRoute from './componentes/ProtectedRoute.jsx'

const router = createBrowserRouter([
  {
    element: (
      <AuthProvider>
        <Header />
        <Outlet />
        <Footer />
      </AuthProvider>
    ),
    children: [
      { index: true, element: <Inicio /> },
      { path: "nosotros", element: <Nosotros /> },
      { path: "centros", element: <Centros /> },
      { path: "donacion", element: <Donacion /> },
      { path: "necesidades", element: <Necesidades /> },
      { path: "registro", element: <Registro /> },
      { path: "dashboard", element: <ProtectedRoute requiredRole="admin"><BackOffice /></ProtectedRoute> },
      { path: "login", element: <Login /> },
      { path: "perfil", element: <ProtectedRoute><Perfil /></ProtectedRoute> },
      { path: "transparencia", element: <Transparencia /> },
      { path: "222", element: <Importante /> },
      { path: "*", element: <h1 className="text-center mt-5">404 - Página no encontrada</h1> },
    ]
  }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
)
