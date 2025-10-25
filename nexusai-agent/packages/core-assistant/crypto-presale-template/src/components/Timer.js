import React, { useState, useEffect } from 'react';

const Timer = ({ endTime }) => {
  const [timeLeft, setTimeLeft] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0
  });

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date().getTime();
      const distance = endTime - now;

      setTimeLeft({
        days: Math.floor(distance / (1000 * 60 * 60 * 24)),
        hours: Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
        minutes: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
        seconds: Math.floor((distance % (1000 * 60)) / 1000)
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [endTime]);

  return (
    <div className="presale-timer">
      <h3>Presale Ends In:</h3>
      <div className="timer-grid">
        <div className="timer-item">
          <span>{timeLeft.days}</span>
          <label>Days</label>
        </div>
        <div className="timer-item">
          <span>{timeLeft.hours}</span>
          <label>Hours</label>
        </div>
        <div className="timer-item">
          <span>{timeLeft.minutes}</span>
          <label>Minutes</label>
        </div>
        <div className="timer-item">
          <span>{timeLeft.seconds}</span>
          <label>Seconds</label>
        </div>
      </div>
    </div>
  );
};

export default Timer;