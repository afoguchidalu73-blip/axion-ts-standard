class WorldModel:
    def __init__(self, initial_val):
        self.state = initial_val
        self.uncertainty = 0.0

    def predict(self, action):
        """Pure prediction logic."""
        if action['type'] == 'TRANSFER':
            return self.state - action['amount']
        return self.state

    def update(self, actual_val):
        """Corrects internal belief and tracks prediction error."""
        error = abs(self.state - actual_val)
        self.state = actual_val
        # Uncertainty grows if reality deviates from our previous state
        self.uncertainty = (self.uncertainty * 0.8) + (error * 0.2)
        return error
      
