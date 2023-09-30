import { useState } from 'react'
import React from 'react';



export default function Album({album}) {
    return (
        <li>
            <p>Album:</p>
            <p>{album.artist}</p>
            <p>{album.title}</p>
            <p>{album.sales}</p>
        </li>
    )
}