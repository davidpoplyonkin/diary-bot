import Chart from './Chart';

function App() {
  const name = window.Telegram?.WebApp?.initDataUnsafe?.user?.first_name
  
  return (
    <div>
      <p>{name}</p>
      <Chart />
    </div>
  );
}

export default App;