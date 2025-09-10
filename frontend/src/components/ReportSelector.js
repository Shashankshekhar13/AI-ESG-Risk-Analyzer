import React from 'react';

const ReportSelector = ({ reports, onSelectReport, selectedReport }) => {
  return (
    <aside className="report-selector">
      <h2>Available Reports</h2>
      {reports.length > 0 ? (
        <ul>
          {reports.map(reportName => (
            <li 
              key={reportName} 
              className={reportName === selectedReport ? 'selected' : ''}
              onClick={() => onSelectReport(reportName)}
            >
              {reportName}
            </li>
          ))}
        </ul>
      ) : (
        <p>Loading reports...</p>
      )}
    </aside>
  );
};

export default ReportSelector;