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
  const [riskThreshold, setRiskThreshold] = useState(0.1);

  // This hook runs once on component mount to fetch the list of available reports.
  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/reports')
      .then(response => response.json())
      .then(data => setReports(data))
      .catch(err => {
        console.error("Error fetching reports:", err);
        setError('Could not connect to the backend. Is the Python server running?');
      });
  }, []);
  
  // This function is triggered when a user clicks on a report name in the sidebar.
  const handleSelectReport = (reportName) => {
    if (reportName === selectedReport) return;
    
    // Reset all states for the new analysis
    setSelectedReport(reportName);
    setIsLoading(true);
    setAnalysisData(null);
    setError(null);
    setCategoryFilter('All');
    setSortConfig({ key: 'negativity_score', direction: 'descending' });
    setRiskThreshold(0.1);

    // Fetch the detailed analysis for the selected report from the backend API.
    fetch(`http://127.0.0.1:5000/api/analyze?report=${encodeURIComponent(reportName)}`)
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
        setError('Failed to analyze the report. Please check the backend server logs.');
        setIsLoading(false);
      });
  };

  // useMemo is a performance optimization. This block of code will only re-run when its
  // dependencies (the data or the filters) change, preventing unnecessary re-renders of the table.
  const processedData = useMemo(() => {
    if (!analysisData || !analysisData.findings) {
      return null;
    }

    let filteredData = [...analysisData.findings];

    // 1. Apply category filter from the dropdown
    if (categoryFilter !== 'All') {
      filteredData = filteredData.filter(item => item.category === categoryFilter);
    }
    
    // 2. Apply risk threshold filter from the slider
    if (riskThreshold > 0.1) {
      filteredData = filteredData.filter(item => item.negativity_score >= riskThreshold);
    }

    // 3. Apply sorting based on table header clicks
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