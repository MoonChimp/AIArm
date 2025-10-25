import React from 'react';

const PresaleHeader = () => {
  return (
    <header className="presale-header">
      <h1>Token Presale</h1>
      <div className="token-basics">
        <span>Token Symbol: YOUR_TOKEN</span>
        <span>Token Contract: 0x...</span>
      </div>
    </header>
  );
};

export default PresaleHeader;