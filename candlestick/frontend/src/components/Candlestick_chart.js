// frontend/src/components/CandlestickChart.js
import React, { useState, useEffect } from 'react';
import Chart from 'react-apexcharts';

const CandlestickChart = () => {
  const [options, setOptions] = useState({});
  const [series, setSeries] = useState([{ data: [] }]);
  const [symbol, setSymbol] = useState('BTCUSDT');
  const [interval, setInterval] = useState('1h');

  useEffect(() => {
    fetchCandles();
  }, [symbol, interval]);

  const fetchCandles = async () => {
    const response = await fetch(
      `/api/candles/?symbol=${symbol}&interval=${interval}`
    );
    const data = await response.json();

    const chartData = data.candles.map(candle => ({
      x: new Date(candle.time * 1000),
      y: [candle.open, candle.high, candle.low, candle.close]
    }));

    setSeries([{  chartData }]);
    setOptions({
      chart: { type: 'candlestick', height: 400 },
      title: { text: `${symbol} ${interval} Chart`, align: 'left' },
      xaxis: { type: 'datetime' },
      yaxis: { tooltip: { enabled: true } }
    });
  };

  return (
    <div>
      <h1>Crypto Candlestick Chart</h1>
      <div>
        <input
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Symbol (e.g. BTCUSDT)"
        />
        <select value={interval} onChange={(e) => setInterval(e.target.value)}>
          <option value="1m">1 minute</option>
          <option value="5m">5 minutes</option>
          <option value="15m">15 minutes</option>
          <option value="1h">1 hour</option>
          <option value="4h">4 hours</option>
          <option value="1d">1 day</option>
        </select>
      </div>
      {options && (
        <Chart options={options} series={series} type="candlestick" height={400} />
      )}
    </div>
  );
};

export default CandlestickChart;