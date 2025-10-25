import React, { useState, useEffect } from 'react';
import './App.css';
import PresaleHeader from './components/PresaleHeader';
import TokenInfo from './components/TokenInfo';
import PresaleForm from './components/PresaleForm';
import Timer from './components/Timer';

function App() {
  const [presaleState, setPresaleState] = useState({
    raised: 0,
    goal: 100,
    tokenPrice: 0.001,
    minContribution: 0.1,
    maxContribution: 10,
    presaleEnd: new Date('2024-12-31').getTime()
  });

  return (
    <div className="App">
      <PresaleHeader />
      <div className="presale-container">
        <TokenInfo />
        <Timer endTime={presaleState.presaleEnd} />
        <PresaleForm 
          presaleState={presaleState}
          setPresaleState={setPresaleState}
        />
      </div>
    </div>
  );
}

export default App;