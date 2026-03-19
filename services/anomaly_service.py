class AnomalyService:

    def detect_spike(self, txn, avg):
        return txn["amount"] > 2 * avg