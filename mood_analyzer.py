# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

from typing import List, Optional
import re

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

        # Simple negation words
        self.negation_words = {"not", "no", "never", "isnt", "isn't", "dont", "don't", "cant", "can't"}

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Improvements:
          - strip whitespace
          - lowercase
          - remove most punctuation
          - keep simple emoji tokens like :) :( 😂 💀
        """
        cleaned = text.strip().lower()

        # Normalize curly apostrophes to straight apostrophes
        cleaned = cleaned.replace("’", "'")

        # Keep words, contractions, and a few common emoji/emoticon tokens
        tokens = re.findall(r"[a-zA-Z']+|:\)|:\(|😂|💀|🥲", cleaned)

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        Modeling improvement implemented:
          - simple negation handling ("not happy" -> negative,
            "not bad" -> positive)
          - simple emoji handling for a few common cases
        """
        tokens = self.preprocess(text)
        score = 0
        i = 0

        while i < len(tokens):
            token = tokens[i]

            # Handle negation + next word
            if token in self.negation_words and i + 1 < len(tokens):
                next_token = tokens[i + 1]

                if next_token in self.positive_words:
                    score -= 1
                    i += 2
                    continue
                elif next_token in self.negative_words:
                    score += 1
                    i += 2
                    continue

            # Regular word scoring
            if token in self.positive_words:
                score += 1
            elif token in self.negative_words:
                score -= 1

            # Simple emoji / emoticon signals
            elif token in {":)", "😂"}:
                score += 1
            elif token in {":(", "🥲", "💀"}:
                score -= 1

            i += 1

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
      """
      Turn the numeric score for a piece of text into a mood label.

      Rules:
        - both positive and negative signals -> "mixed"
        - only positive signals -> "positive"
        - only negative signals -> "negative"
        - no signals -> "neutral"
      """
      tokens = self.preprocess(text)

      positive_seen = 0
      negative_seen = 0
      i = 0

      while i < len(tokens):
          token = tokens[i]

          # Handle negation + next word
          if token in self.negation_words and i + 1 < len(tokens):
              next_token = tokens[i + 1]

              if next_token in self.positive_words:
                  negative_seen += 1
                  i += 2
                  continue
              elif next_token in self.negative_words:
                  positive_seen += 1
                  i += 2
                  continue

          if token in self.positive_words or token in {":)", "😂"}:
              positive_seen += 1
          elif token in self.negative_words or token in {":(", "🥲", "💀"}:
              negative_seen += 1

          i += 1

      if positive_seen > 0 and negative_seen > 0:
          return "mixed"
      elif positive_seen > 0:
          return "positive"
      elif negative_seen > 0:
          return "negative"
      else:
          return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0
        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token in self.negation_words and i + 1 < len(tokens):
                next_token = tokens[i + 1]

                if next_token in self.positive_words:
                    negative_hits.append(f"{token} {next_token}")
                    score -= 1
                    i += 2
                    continue
                elif next_token in self.negative_words:
                    positive_hits.append(f"{token} {next_token}")
                    score += 1
                    i += 2
                    continue

            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            elif token in self.negative_words:
                negative_hits.append(token)
                score -= 1
            elif token in {":)", "😂"}:
                positive_hits.append(token)
                score += 1
            elif token in {":(", "🥲", "💀"}:
                negative_hits.append(token)
                score -= 1

            i += 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
