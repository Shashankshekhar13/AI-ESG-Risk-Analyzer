import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register the necessary components for Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const RiskChart = ({ data }) => {
  // Process the data to count risks per category
  const categoryCounts = data.reduce((acc, item) => {
    acc[item.category] = (acc[item.category] || 0) + 1;
    return acc;
  }, {});

  const chartData = {
    labels: Object.keys(categoryCounts),
    datasets: [
      {
        label: 'Number of Risks Flagged',
        data: Object.values(categoryCounts),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)', // Environmental
          'rgba(54, 162, 235, 0.6)', // Social
          'rgba(255, 206, 86, 0.6)', // Governance
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Risk Distribution by Category',
        font: {
            size: 18
        }
      },
    },
  };

  return <Bar data={chartData} options={options} />;
};

export default RiskChart;