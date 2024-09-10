import time
from collections import defaultdict
import threading

class Metrics:
    def __init__(self):
        self.predictions = defaultdict(int)
        self.latencies = []
        self.lock = threading.Lock()

    def record_prediction(self, class_name, latency):
        with self.lock:
            self.predictions[class_name] += 1
            self.latencies.append(latency)

    def get_metrics(self):
        with self.lock:
            total_predictions = sum(self.predictions.values())
            avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
            return {
                "total_predictions": total_predictions,
                "predictions_by_class": dict(self.predictions),
                "average_prediction_latency": avg_latency,
            }

metrics = Metrics()