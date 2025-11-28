import numpy as np
from sklearn.ensemble import IsolationForest
from .models import ScanLog

class GhostBrain:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1) # Assume 10% of data might be anomalies
        self.is_trained = False

    def train(self):
        """
        Fetches historical scan data to understand 'Normal' traffic patterns.
        """
        # Get last 50 scans (enough to learn a pattern)
        logs = ScanLog.objects.all().order_by('-timestamp')[:50]
        
        if len(logs) < 5:
            # Not enough data to learn yet
            self.is_trained = False
            return

        # Prepare data for Scikit-Learn (Needs 2D array: [[5], [6], [5], ...])
        data = np.array([log.devices_online for log in logs]).reshape(-1, 1)
        
        self.model.fit(data)
        self.is_trained = True

    def check_anomaly(self, current_device_count):
        """
        Returns True if the current count is anomalous.
        """
        if not self.is_trained:
            self.train()
            if not self.is_trained:
                return False # Default to Safe if not enough data

        # Scikit-Learn expects a 2D array for prediction
        input_data = np.array([[current_device_count]])
        
        # Predict returns: 1 for Normal, -1 for Anomaly
        prediction = self.model.predict(input_data)[0]
        
        return prediction == -1