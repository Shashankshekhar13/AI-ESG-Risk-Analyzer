import { useState, useEffect, useMemo } from 'react';
import ReportSelector from './components/ReportSelector';
import AnalysisView from './components/AnalysisView';
import './App.css';

// --- PRODUCTION API URL ---
const API_BASE_URL = 'https://ai-esg-risk-analyzer-backend.onrender.com';

function App() {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [categoryFilter, setCategoryFilter] = useState('All');
  const [sortConfig, setSortConfig] = useState({ key: 'negativity_score', direction: 'descending' });
  const [riskThreshold, setRiskThreshold] = useState(0.1);

  // Fetch the list of available reports when the app loads
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/reports`)
      .then(response => response.json())
      .then(data => setReports(data))
      .catch(err => {
        console.error("Error fetching reports:", err);
        setError('Could not connect to the backend server. It may be starting up.');
      });
  }, []);
  
  // Handle the selection of a new report to analyze
  const handleSelectReport = (reportName) => {
    if (reportName === selectedReport) return;
    
    setSelectedReport(reportName);
    setIsLoading(true);
    setAnalysisData(null);
    setError(null);
    setCategoryFilter('All');
    setSortConfig({ key: 'negativity_score', direction: 'descending' });
    setRiskThreshold(0.1);

    // Fetch the detailed analysis for the selected report from the live backend
    fetch(`${API_BASE_URL}/api/analyze?report=${encodeURIComponent(reportName)}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setAnalysisData(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error("Error fetching analysis:", err);
        setError('Failed to analyze the report. The server may be busy. Please try again.');
        setIsLoading(false);
      });
  };

  // Memoized calculation for filtering and sorting the display data
  const processedData = useMemo(() => {
    if (!analysisData || !analysisData.findings) {
      return null;
    }
    let filteredData = [...analysisData.findings];
    if (categoryFilter !== 'All') {
      filteredData = filteredData.filter(item => item.category === categoryFilter);
    }
    if (riskThreshold > 0.1) {
      filteredData = filteredData.filter(item => item.negativity_score >= riskThreshold);
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
  }, [analysisData, categoryFilter, sortConfig, riskThreshold]);

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
          riskThreshold={riskThreshold}
          setRiskThreshold={setRiskThreshold}
        />
      </main>
    </div>
  );
}

export default App;