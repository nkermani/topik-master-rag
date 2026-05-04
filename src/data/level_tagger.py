# src/data/level_tagger.py

"""Auto-tag content with TOPIK levels based on vocabulary difficulty."""
import re
from src.utils.logger import Logger


class LevelTagger:
    """Assign TOPIK levels to content based on vocabulary analysis."""

    LEVEL_KEYWORDS = {
        1: ["입니다", "있습니다", "감사합니다"],
        2: ["~기 때문에", "~는 동안", "그런데"],
        3: ["~거든", "~기에", "그러나"],
        4: ["~는 바", "~함에 있어", "아울러"],
        5: ["~현", "~적", "~성"],
        6: ["~담론", "~화두", "~궤"],
    }

    def __init__(self):
        self.logger = Logger("level_tagger").logger

    def tag_content(self, content: str) -> int:
        """Determine TOPIK level based on content complexity."""
        level_scores = {}
        for level, keywords in self.LEVEL_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in content)
            level_scores[level] = score

        return max(level_scores, key=level_scores.get) if any(level_scores.values()) else 1
