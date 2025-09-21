import React from 'react';
import RiskChart from './RiskChart';

const AnalysisView = ({
  data, isLoading, error, selectedReport,
  categoryFilter, setCategoryFilter,
  sortConfig, setSortConfig,
  originalData,
  riskThreshold, setRiskThreshold
}) => {

  if (isLoading) {
    return <section className="analysis-view"><div className="loader">Analyzing Report...</div></section>;
  }

  if (error) {
    return <section className="analysis-view"><div className="error">{error}</div></section>;
  }

  if (!selectedReport) {
    return <section className="analysis-view"><p>Please select a report from the left to begin analysis.</p></section>;
  }

  if (!originalData || !originalData.findings || originalData.findings.length === 0) {
    return (
      <section className="analysis-view">
        <h2>Analysis for: <strong>{selectedReport}</strong></h2>
        <p>Analysis complete. No significant negative-sentiment risks were flagged in this report.</p>
      </section>
    );
  }
  
  // --- BUG FIX: Correctly calculate the highest risk category by COUNT ---
  // First, count the number of risks in each category
  const categoryCounts = originalData.findings.reduce((acc, item) => {
    acc[item.category] = (acc[item.category] || 0) + 1;
    return acc;
  }, {});

  // Then, find the category name with the highest count
  const highestRiskCategory = Object.keys(categoryCounts).reduce((a, b) => 
    categoryCounts[a] > categoryCounts[b] ? a : b,
    Object.keys(categoryCounts)[0] || '' // Add a fallback for safety
  );
  
  // We still need the single most severe sentence for the "Top Negativity Score" card
  const mostSevereRiskItem = originalData.findings.reduce(
    (max, item) => (item.negativity_score > max.negativity_score ? item : max),
    originalData.findings[0]
  );
  // --- END OF BUG FIX ---
  
  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };
  
  return (
    <section className="analysis-view">
      <h2>Analysis for: <strong>{selectedReport}</strong></h2>
      
      <div className="summary-cards">
        <div className="card score-card">
          <span className="card-value">{originalData.overall_risk_score}</span>
          <span className="card-label">Overall Risk Score / 10</span>
        </div>
        <div className="card">
          <span className="card-value">{originalData.total_risks_found}</span>
          <span className="card-label">Total Risks Found</span>
        </div>
        <div className="card">
          {/* Use the new, correct variable here */}
          <span className="card-value">{highestRiskCategory}</span>
          <span className="card-label">Highest Risk Category</span>
        </div>
        <div className="card">
          {/* Use the new, correct variable here */}
          <span className="card-value">{mostSevereRiskItem.negativity_score}</span>
          <span className="card-label">Top Negativity Score</span>
        </div>
      </div>

      <div className="chart-container">
        <RiskChart data={originalData.findings} />
      </div>

      <div className="analysis-controls">
        <h3>Detailed Findings ({data ? data.length : 0} results)</h3>
        <div className="controls-wrapper">
          <label htmlFor="category-filter">Filter by Category:</label>
          <select 
            id="category-filter"
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
          >
            <option value="All">All Categories</option>
            <option value="Environmental">Environmental</option>
            <option value="Social">Social</option>
            <option value="Governance">Governance</option>
          </select>
          <label htmlFor="threshold-slider">Min. Severity:</label>
          <input 
            type="range" 
            id="threshold-slider"
            min="0.1" 
            max="1.0" 
            step="0.05"
            value={riskThreshold}
            onChange={(e) => setRiskThreshold(parseFloat(e.target.value))}
          />
          <span>{riskThreshold.toFixed(2)}</span>
          <button className="export-button" onClick={() => { /* Export function will be here */ }}>Export as CSV</button>
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th onClick={() => requestSort('category')}>Category</th>
              <th onClick={() => requestSort('keyword')}>Keyword</th>
              <th onClick={() => requestSort('negativity_score')}>Negativity ↓↑</th>
              <th>Flagged Sentence</th>
            </tr>
          </thead>
          <tbody>
            {data && data.length > 0 ? (
              data.map((item, index) => (
                <tr key={index}>
                  <td><span className={`pill ${item.category.toLowerCase()}`}>{item.category}</span></td>
                  <td>{item.keyword}</td>
                  <td>{item.negativity_score}</td>
                  <td>{item.sentence}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4">No results match the current filter.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default AnalysisView;