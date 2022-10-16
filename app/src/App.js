import React from 'react';
import './App.css';
import Select from 'react-select'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis } from 'recharts';


let options = [{value: null, label: "Выберите торговый инструмент"}]
for (let i = 0; i < 100; i++) {
  options.push({value: `ticker${i > 9 ? i : '0'+String(i)}`, label: `Ticker ${i}`})
}

function App () {
  const source = new EventSource('http://localhost:5000/events');
  const [data, setData] = React.useState([])
  const [option, setOption] = React.useState(null)

  const handleData = async (e) => {
    setData([...data, JSON.parse(e.data)])    
  }

  const handleOption = (e) => {
    if (option) {
      axios.get(`http://localhost:5000/stop/${option.value}`,{headers: {'Access-Control-Allow-Origin': '*'}})
      .then(
        () => {
          console.log('Scheduler stoped')
        },
        (error) => {
          console.log(error)
        }
      )
    }
    setOption(e)
    setData([])
    axios.get(`http://localhost:5000/start/${e.value}`,{headers: {'Access-Control-Allow-Origin': '*'}})
    .then(
      (result) => {
        setData(result.data)
        console.log('Scheduler started')
      },
      (error) => {
        console.log(error)
      }
    )
  }

  React.useEffect(() => {
    source.onmessage = handleData
    return () => {
      source.close();
    };
  })
  return (
    <>
      <Select options={options} value={option} onChange={handleOption}/>
      <LineChart width={1000} height={300} data={data}>
        <Line type="monotone" dataKey="price" stroke="#8884d8" strokeWidth={2} />
        <XAxis dataKey="timestamp" />
        <YAxis dataKey="price"/>
      </LineChart>
    </>
  );
}

export default App;
