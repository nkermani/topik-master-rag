# main/query.py

"""Main entry point for querying the RAG system."""
import argparse
from src.retrieval.query import QueryPipeline
from src.utils.logger import Logger


def main():
    """Query the TOPIK Master RAG system."""
    parser = argparse.ArgumentParser(description="Query TOPIK RAG")
    parser.add_argument("query", type=str, help="Your question in English or Korean")
    parser.add_argument("--level", type=int, choices=range(1, 7),
                        help="TOPIK level (1-6) to filter results")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    args = parser.parse_args()

    logger = Logger("main_query").logger
    pipeline = QueryPipeline()

    logger.info(f"Querying: {args.query} (Level: {args.level})")
    results = pipeline.search(args.query, topik_level=args.level, k=args.top_k)

    print(f"\n🔍 Top {len(results)} results for: {args.query}\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result[:200]}...\n")


if __name__ == "__main__":
    main()
