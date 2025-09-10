import { useState, useEffect, useMemo } from 'react';
import ReportSelector from './components/ReportSelector';
import AnalysisView from './components/AnalysisView';
import './App.css';

function App() {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [sortConfig, setSortConfig] = useState({ key: 'negativity_score', direction: 'descending' });

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/reports')
      .then(response => response.json())
      .then(data => setReports(data))
      .catch(err => {
        console.error("Error fetching reports:", err);
        setError('Could not connect to the backend. Is the Python server running?');
      });
  }, []);
  
  const handleSelectReport = (reportName) => {
    if (reportName === selectedReport) return;
    
    setSelectedReport(reportName);
    setIsLoading(true);
    setAnalysisData(null);
    setError(null);
    setCategoryFilter('All');
    setSortConfig({ key: 'negativity_score', direction: 'descending' });

    fetch(`http://127.0.0.1:5000/api/analyze?report=${encodeURIComponent(reportName)}`)
      .then(response => response.json())
      .then(data => {
        setAnalysisData(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error("Error fetching analysis:", err);
        setError('Failed to analyze the report.');
        setIsLoading(false);
      });
  };

  const processedData = useMemo(() => {
    if (!analysisData) return null;
    let filteredData = [...analysisData];
    if (categoryFilter !== 'All') {
      filteredData = filteredData.filter(item => item.category === categoryFilter);
    }
    filteredData.sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) {
        return sortConfig.direction === 'ascending' ? -1 : 1;
      }
      if (a[sortConfig.key] > b[sortConfig.key]) {
        return sortConfig.direction === 'ascending' ? 1 : -1;
      }
      return 0;
    });
    return filteredData;
  }, [analysisData, categoryFilter, sortConfig]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ESG Risk Analysis Dashboard</h1>
      </header>
      <main className="App-main">
        <ReportSelector 
          reports={reports} 
          onSelectReport={handleSelectReport} 
          selectedReport={selectedReport}
        />
        <AnalysisView 
          data={processedData} 
          isLoading={isLoading}
          error={error}
          selectedReport={selectedReport}
          categoryFilter={categoryFilter}
          setCategoryFilter={setCategoryFilter}
          sortConfig={sortConfig}
          setSortConfig={setSortConfig}
          originalData={analysisData}
        />
      </main>
    </div>
  );
}

export default App;