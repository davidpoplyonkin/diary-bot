import Chart from './Chart';

function App() {
  window.Telegram.WebApp.setHeaderColor('secondary_bg_color');
  window.Telegram.WebApp.requestFullscreen();

  return <Chart />;
}

export default App;