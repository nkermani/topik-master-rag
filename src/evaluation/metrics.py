"""Ragas metrics for evaluating RAG performance."""
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision
from src.utils.logger import Logger


class RAGEvaluator:
    """Evaluate RAG system using Ragas framework."""

    def __init__(self):
        self.logger = Logger("evaluator").logger
        self.metrics = [faithfulness, context_precision]

    def evaluate_dataset(self, dataset: dict):
        """Run evaluation on a dataset dict with keys: questions, contexts, answers."""
        try:
            result = evaluate(dataset=dataset, metrics=self.metrics)
            self.logger.info(f"Evaluation complete: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Evaluation failed: {e}")
            return None

    def print_results(self, results):
        """Pretty print evaluation results."""
        if results:
            for metric, score in results.items():
                print(f"{metric}: {score:.3f}")
