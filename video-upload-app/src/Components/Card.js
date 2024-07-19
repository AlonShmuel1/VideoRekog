// Card.js
import React from 'react';
import './Card.css';

function Card({ image, label,confidence,onClick }) {
  return (
    <div className="card" onClick={onClick}>
      <img src={image} alt={label} className="card-image" />
      <p className="card-label">Object:{label}</p>
      <p className='card-confidence'>Confidence:{confidence}</p>
    </div>
  );
}

export default Card;
