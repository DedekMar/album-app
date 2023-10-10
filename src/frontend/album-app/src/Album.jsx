/* eslint-disable react/prop-types */
//import { useState } from "react";
//import React from "react";

export default function Album({ album, onDetail }) {
  return (
    <li>
      <p>Album:</p>
      <p>{album.artist}</p>
      <p>{album.title}</p>
      <p>{album.sales}</p>
      <button onClick={(e) => onDetail(album, e)}>Detail</button>
    </li>
  );
}
