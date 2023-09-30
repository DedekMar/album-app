import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Album from "./Album.jsx"

function App() {
  const [count, setCount] = useState(0)
  const [data, setData] = useState([])
  const [albums, setAlbums] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/albums/');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const jsonData = await response.json();
        console.log(jsonData)
        setData(jsonData);
        setAlbums(jsonData)
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    };

    // Call the fetchData function when the component is mounted
    fetchData();
  }, []); 

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>

      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <ul>
      {albums.map((album) => (
        <Album key={album.id} album={album} /> 
      ))}
      </ul>
    </>
  )
}

export default App
