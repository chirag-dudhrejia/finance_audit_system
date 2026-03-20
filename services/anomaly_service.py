class AnomalyService:
    """Anomaly detection requires user-specific historical data.

    Without historical spending patterns per user, statistical thresholds
    are meaningless (one user's normal spend is another's anomaly).

    TODO: Implement after building historical data accumulation.
    """

    def detect_all(self, records):
        return []
