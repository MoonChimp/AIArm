import React, { useState } from 'react';

const PresaleForm = ({ presaleState, setPresaleState }) => {
  const [contribution, setContribution] = useState('');

  const handleContribute = (e) => {
    e.preventDefault();
    // Here you would typically integrate with Web3 and smart contract
    console.log(`Contributing ${contribution} ETH`);
    setPresaleState({
      ...presaleState,
      raised: presaleState.raised + parseFloat(contribution)
    });
  };

  return (
    <div className="presale-form">
      <div className="progress-bar">
        <div 
          className="progress" 
          style={{ width: `${(presaleState.raised / presaleState.goal) * 100}%` }}
        ></div>
      </div>
      <div className="presale-stats">
        <p>Raised: {presaleState.raised} ETH / {presaleState.goal} ETH</p>
      </div>
      <form onSubmit={handleContribute}>
        <div className="input-group">
          <input
            type="number"
            value={contribution}
            onChange={(e) => setContribution(e.target.value)}
            min={presaleState.minContribution}
            max={presaleState.maxContribution}
            step="0.1"
            placeholder="Amount in ETH"
          />
          <button type="submit">Contribute</button>
        </div>
        <div className="contribution-limits">
          <p>Min: {presaleState.minContribution} ETH</p>
          <p>Max: {presaleState.maxContribution} ETH</p>
        </div>
      </form>
    </div>
  );
};

export default PresaleForm;