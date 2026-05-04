"""Main entry point for RAG evaluation."""
import argparse
from src.evaluation.metrics import RAGEvaluator
from src.utils.logger import Logger


def main():
    """Run Ragas evaluation on the RAG system."""
    parser = argparse.ArgumentParser(description="Evaluate TOPIK RAG")
    parser.add_argument("--dataset", type=str, help="Path to evaluation dataset JSON")
    args = parser.parse_args()

    logger = Logger("main_eval").logger
    evaluator = RAGEvaluator()

    dataset = {"questions": [], "contexts": [], "answers": []}
    if args.dataset:
        import json
        with open(args.dataset, "r") as f:
            dataset = json.load(f)

    logger.info("Starting evaluation...")
    results = evaluator.evaluate_dataset(dataset)
    evaluator.print_results(results)


if __name__ == "__main__":
    main()
