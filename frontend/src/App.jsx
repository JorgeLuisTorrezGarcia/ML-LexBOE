import { useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [texto, setTexto] = useState('')
  const [rama, setRama] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  async function clasificar(e) {
    e.preventDefault()
    setError(null)
    setRama(null)

    if (texto.trim().length < 20) {
      setError('El texto es demasiado corto (mínimo 20 caracteres).')
      return
    }

    setCargando(true)
    try {
      const res = await fetch(`${API_URL}/api/clasificar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texto }),
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || 'Error del servidor')
      }
      setRama(data.rama)
    } catch (err) {
      setError(err.message || 'No se pudo conectar con el servidor.')
    } finally {
      setCargando(false)
    }
  }

  function limpiar() {
    setTexto('')
    setRama(null)
    setError(null)
  }

  return (
    <main className="contenedor">
      <header className="cabecera">
        <div className="marca">
          <span className="logo" aria-hidden="true">§</span>
          <div>
            <h1>LexBOE</h1>
            <p className="tagline">Clasificador de ramas del Boletín Oficial del Estado</p>
          </div>
        </div>
      </header>

      <form onSubmit={clasificar} className="tarjeta">
        <div className="campo">
          <label htmlFor="texto">Texto a clasificar</label>
          <textarea
            id="texto"
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            placeholder="Pega aquí un fragmento del BOE…"
            rows={8}
            disabled={cargando}
          />
          <div className="contador">{texto.length} caracteres</div>
        </div>

        <div className="acciones">
          <button
            type="button"
            className="btn-secundario"
            onClick={limpiar}
            disabled={cargando || (!texto && !rama && !error)}
          >
            Limpiar
          </button>
          <button type="submit" className="btn-primario" disabled={cargando || !texto.trim()}>
            {cargando ? 'Clasificando…' : 'Clasificar'}
          </button>
        </div>
      </form>

      {error && <p className="error" role="alert">{error}</p>}

      {rama && (
        <div className="resultado" role="status">
          <span className="etiqueta">Rama predicha</span>
          <strong className="rama">{rama}</strong>
        </div>
      )}

      <footer className="pie">
        <p>
          Modelo TF-IDF + LinearSVC entrenado sobre el dataset{' '}
          <a href="https://huggingface.co/datasets/BSC-LT/LexBOE" target="_blank" rel="noopener noreferrer">
            BSC-LT/LexBOE
          </a>{' '}
          (Hugging Face).
        </p>
        <details className="cita">
          <summary>Citar el dataset</summary>
          <pre>{`@article{tamayo2026mrbert,
  title={MrBERT: Modern Multilingual Encoders via Vocabulary, Domain, and Dimensional Adaptation},
  author={Tamayo, Daniel and Lacunza, I{\\~n}aki and Rivera-Hidalgo, Paula and Da Dalt, Severino and Aula-Blasco, Javier and Gonzalez-Agirre, Aitor and Villegas, Marta},
  journal={arXiv preprint arXiv:2602.21379},
  year={2026}
}`}</pre>
        </details>
      </footer>
    </main>
  )
}

export default App
