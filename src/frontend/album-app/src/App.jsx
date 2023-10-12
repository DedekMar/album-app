import { useState, useEffect } from "react";
//import reactLogo from "./assets/react.svg";
//import viteLogo from "/vite.svg";
import "./App.css";
import Album from "./Album.jsx";
import AlbumDetail from "./albumDetail";
import AlbumSearch from "./AlbumSearch";

function App() {
  //const [count, setCount] = useState(0);
  //const [data, setData] = useState([]);
  const [albums, setAlbums] = useState([]);
  const [isDetail, setIsDetail] = useState(false);
  const [selectedAlbumId, setSelectedAlbumId] = useState(null);
  const [albumSearchText, setAlbumSearchText] = useState("");
  const [albumsSearchResult, setAlbumsSearchResult] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/albums/");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const jsonData = await response.json();
        console.log(jsonData);
        //setData(jsonData);
        setAlbums(jsonData);
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
      }
    };

    // Call the fetchData function when the component is mounted
    fetchData();
  }, []);

  function showDetail(album, e) {
    console.log(album, e);
    setIsDetail(true);
    setSelectedAlbumId(album.id);
  }

  function handleBackFromDetail(e) {
    console.log(e);
    setIsDetail(false);
    setSelectedAlbumId(null);
  }
  function handleSearchTextChange(e) {
    //console.log(e);
    setAlbumSearchText(e.target.value);
    if (e.target.value.length == 0) {
      setAlbumsSearchResult([]);
    }
  }

  async function handleSearch() {
    //console.log(e);
    const res = await fetch(
      `http://127.0.0.1:8000/album/title/?title=${albumSearchText}`
    );
    //console.log(res);
    const albumSearchData = await res.json();
    console.log(albumSearchData);
    setAlbumsSearchResult(albumSearchData);
  }

  return (
    <>
      <div>
        <AlbumSearch
          onTextChange={handleSearchTextChange}
          onSearch={handleSearch}
          searchValue={albumSearchText}
        />
        {albumsSearchResult.length > 0 ? (
          <ul>
            {albumsSearchResult.map((album) => (
              <Album key={album.id} album={album} onDetail={showDetail} />
            ))}
          </ul>
        ) : (
          <p>Try searching</p>
        )}
      </div>
      <div>
        {isDetail ? (
          <AlbumDetail
            albumId={selectedAlbumId}
            onBack={handleBackFromDetail}
          />
        ) : (
          <ul>
            {albums.map((album) => (
              <Album key={album.id} album={album} onDetail={showDetail} />
            ))}
          </ul>
        )}
      </div>
    </>
  );
}

export default App;
