import React from 'react';

const TokenInfo = () => {
  return (
    <div className="token-info">
      <h2>Token Information</h2>
      <div className="info-grid">
        <div className="info-item">
          <label>Token Name</label>
          <span>Your Token</span>
        </div>
        <div className="info-item">
          <label>Token Symbol</label>
          <span>YTK</span>
        </div>
        <div className="info-item">
          <label>Total Supply</label>
          <span>1,000,000 YTK</span>
        </div>
        <div className="info-item">
          <label>Presale Rate</label>
          <span>1 ETH = 1000 YTK</span>
        </div>
      </div>
    </div>
  );
};

export default TokenInfo;