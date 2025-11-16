import React, { useState, useEffect } from 'react';
import './TrackChangesPanel.css';

function TrackChangesPanel({ documentId, onAccept, onReject }) {
  const [changes, setChanges] = useState([]);
  const [trackingEnabled, setTrackingEnabled] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (documentId) {
      loadChanges();
    }
  }, [documentId]);

  const loadChanges = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/track-changes/${documentId}`);
      const data = await response.json();
      setChanges(data.changes || []);
      setTrackingEnabled(data.enabled || false);
    } catch (error) {
      console.error('Failed to load changes:', error);
    }
    setLoading(false);
  };

  const toggleTracking = async () => {
    const endpoint = trackingEnabled ? 'disable' : 'enable';
    try {
      await fetch(`http://localhost:8000/api/track-changes/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_id: documentId })
      });
      setTrackingEnabled(!trackingEnabled);
    } catch (error) {
      console.error('Failed to toggle tracking:', error);
    }
  };

  const handleAccept = async (changeId) => {
    try {
      await fetch(`http://localhost:8000/api/track-changes/${changeId}/accept`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_id: documentId })
      });
      onAccept(changeId);
      loadChanges();
    } catch (error) {
      console.error('Failed to accept change:', error);
    }
  };

  const handleReject = async (changeId) => {
    try {
      await fetch(`http://localhost:8000/api/track-changes/${changeId}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_id: documentId })
      });
      onReject(changeId);
      loadChanges();
    } catch (error) {
      console.error('Failed to reject change:', error);
    }
  };

  const handleAcceptAll = async () => {
    try {
      await fetch(`http://localhost:8000/api/track-changes/accept-all`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_id: documentId })
      });
      loadChanges();
    } catch (error) {
      console.error('Failed to accept all changes:', error);
    }
  };

  const handleRejectAll = async () => {
    try {
      await fetch(`http://localhost:8000/api/track-changes/reject-all`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_id: documentId })
      });
      loadChanges();
    } catch (error) {
      console.error('Failed to reject all changes:', error);
    }
  };

  const pendingChanges = changes.filter(c => c.status === 'pending');

  return (
    <div className="track-changes-panel">
      <div className="panel-header">
        <h3>Track Changes</h3>
        <button 
          className={`toggle-tracking ${trackingEnabled ? 'active' : ''}`}
          onClick={toggleTracking}
        >
          {trackingEnabled ? 'ON' : 'OFF'}
        </button>
      </div>

      {trackingEnabled && (
        <div className="tracking-actions">
          <button onClick={handleAcceptAll} disabled={pendingChanges.length === 0}>
            Accept All
          </button>
          <button onClick={handleRejectAll} disabled={pendingChanges.length === 0}>
            Reject All
          </button>
          <button onClick={loadChanges}>
            Refresh
          </button>
        </div>
      )}

      <div className="changes-list">
        {loading ? (
          <p className="loading">Loading changes...</p>
        ) : changes.length === 0 ? (
          <p className="no-changes">No changes tracked</p>
        ) : (
          changes.map((change, index) => (
            <div key={index} className={`change-item ${change.status}`}>
              <div className="change-header">
                <span className={`change-type ${change.type}`}>
                  {change.type.toUpperCase()}
                </span>
                <span className="change-user">{change.user}</span>
              </div>
              
              <div className="change-content">
                {change.content}
              </div>
              
              <div className="change-meta">
                <span className="change-time">
                  {new Date(change.timestamp).toLocaleString()}
                </span>
                <span className="change-status">{change.status}</span>
              </div>

              {change.status === 'pending' && (
                <div className="change-actions">
                  <button 
                    className="accept-btn"
                    onClick={() => handleAccept(change.id)}
                  >
                    ✓ Accept
                  </button>
                  <button 
                    className="reject-btn"
                    onClick={() => handleReject(change.id)}
                  >
                    ✕ Reject
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default TrackChangesPanel;
