//import React from "react";
import { useState, useEffect } from "react";

// eslint-disable-next-line react/prop-types
export default function AlbumDetail({ albumId, onBack }) {
  const [albumDetail, setAlbumDetail] = useState(null);
  const [isLoading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/album/?id=" + albumId
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const jsonData = await response.json();
        console.log(jsonData);
        setAlbumDetail(jsonData);
        //setTimeout(() => setLoading(false), 2000);
        setLoading(false);
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
      }
    };

    // Call the fetchData function when the component is mounted
    fetchData();
  }, [albumId]);
  return (
    <>
      {isLoading ? (
        <div>Loading</div>
      ) : (
        <div>
          <p>{albumDetail.title}</p>
        </div>
      )}
      <button onClick={(e) => onBack(e)}>Back to List</button>
    </>
  );
}
