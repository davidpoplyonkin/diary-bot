import { useState, useEffect } from 'react';
import ReactApexChart from 'react-apexcharts';
import { AxiosError } from 'axios';

import ApiResponse from './types/ApiResponse';
import api from './helpers/api';

function Chart() {
  // Get everything after `?` from the URL
  const queryString = window.location.search;
  
  // Parse it
  const urlParams = new URLSearchParams(queryString);
  const patient = urlParams.get('patient') || '';
  const metric = urlParams.get('metric') || '';

  const tg_palette = window.Telegram.WebApp.themeParams;

  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const chart = {        
    series: [{
      data: [
        { x: '05/06/2014 00:00', y: 111 },
        { x: '05/07/2014 00:00', y: 111 },
        { x: '05/08/2014 00:00', y: 112 },
        { x: '05/09/2014 00:00', y: 113 },
        { x: '05/10/2014 00:00', y: 115 },
        { x: '05/11/2014 00:00', y: 118 },
        { x: '05/12/2014 00:00', y: 113 },
        { x: '05/13/2014 00:00', y: 121 },
        { x: '05/14/2014 00:00', y: 134 },
        { x: '05/15/2014 00:00', y: 155 },
        { x: '05/16/2014 00:00', y: 189 },
        { x: '05/17/2014 00:00', y: 144 },
        { x: '05/18/2014 00:00', y: 233 },
      ]
    }],
    options: {
      chart: {
        foreColor: tg_palette.text_color,
        type: 'area' as const,
        stacked: false,
        zoom: {
          type: 'x' as const,
          enabled: true,
          autoScaleYaxis: true
        },
        toolbar: {
          autoSelected: 'zoom' as const,
          tools: {
            reset: false, // Rescales the chart, but not the axes
            download: false,
          }
        }
      },
      dataLabels: {
        enabled: false
      },
      markers: {
        size: 0,
      },
      title: {
        text: data?.message,
        align: 'left' as const
      },
      fill: {
        colors: [tg_palette.button_color],
        type: 'gradient' as const,
        gradient: {
          shadeIntensity: 1,
          inverseColors: false,
          opacityFrom: 0.5,
          opacityTo: 0,
          stops: [0, 90, 100]
        },
      },
      yaxis: {
        title: {
          text: metric
        },
      },
      xaxis: {
        type: 'datetime' as const,
      },
      tooltip: {
         enabled: false
      }
    },         
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch the data
        const response = await api.get('/')
        setData(response.data);
      } catch (err) {
        const axiosError = err as AxiosError;
        setError(axiosError.message || "An unexpected error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []); // Empty dependency array to run only once on mount

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  
  return (
      <div className="chart">
          <ReactApexChart
            options={chart.options}
            series={chart.series}
            type='area'
            width='100%'
            height='100%'
          />
      </div>
  );
}

export default Chart;