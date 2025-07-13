from typing import Dict, List, Tuple

from .crossclimb_parser import CrossClimbParser
import requests


def edit_distance(a: str, b: str) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


class ClassifierModel:
    def top_k(self, clue: str, length: int, k: int) -> List[Tuple[str, float]]:
        raise NotImplementedError


class DummyClassifier(ClassifierModel):
    """A very small heuristic classifier used for demonstration."""

    def __init__(self, words: List[str]):
        self.words = words

    def top_k(self, clue: str, length: int, k: int) -> List[Tuple[str, float]]:
        options = [w for w in self.words if len(w) == length][:k]
        return [(w, 1 - i * 0.01) for i, w in enumerate(options)]


class ChatGPTClassifier(ClassifierModel):
    """Classifier that queries the GPT-4o model hosted on HuggingFace."""

    def __init__(self, api_token: str, model: str = "openai-community/gpt-4o"):
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def top_k(self, clue: str, length: int, k: int) -> List[Tuple[str, float]]:
        prompt = (
            f"Given the clue '{clue}', provide {k} English words that are exactly "
            f"{length} letters long. Format each on a new line as 'word:score' "
            "where score is a number between 0 and 1."
        )
        response = requests.post(self.api_url, headers=self.headers, json={"inputs": prompt})
        response.raise_for_status()
        text = response.json()[0].get("generated_text", "")
        results: List[Tuple[str, float]] = []
        for line in text.splitlines():
            if ":" not in line:
                continue
            word, score_str = line.split(":", 1)
            try:
                score = float(score_str.strip())
            except ValueError:
                continue
            results.append((word.strip(), score))
            if len(results) >= k:
                break
        return results


class CrossClimbSolver:
    def __init__(self, parser: CrossClimbParser, classifier: ClassifierModel):
        self.parser = parser
        self.classifier = classifier

    def find_best_assignment(
        self, candidates: Dict[int, List[Tuple[str, float]]]
    ) -> Dict[int, str]:
        guess_ids = sorted(candidates.keys())
        best_assignment: Dict[int, str] | None = None
        best_score = 0.0

        def backtrack(index: int, path: Dict[int, str], score: float):
            nonlocal best_assignment, best_score
            if index == len(guess_ids):
                if score > best_score:
                    best_assignment = path.copy()
                    best_score = score
                return
            gid = guess_ids[index]
            for word, s in candidates[gid]:
                if index == 0 or edit_distance(word, path[guess_ids[index - 1]]) == 1:
                    path[gid] = word
                    backtrack(index + 1, path, score * s)
                    path.pop(gid)

        backtrack(0, {}, 1.0)
        return best_assignment or {}

    def solve(self):
        guess_ids = sorted(self.parser.guess_elements.keys())
        candidates: Dict[int, List[Tuple[str, float]]] = {}
        for gid in guess_ids:
            length = self.parser.get_guess_length(gid)
            clue = self.parser.get_clue(gid)
            candidates[gid] = self.classifier.top_k(clue, length, 10)
        assignment = self.find_best_assignment(candidates)
        for gid, word in assignment.items():
            self.parser.submit_guess(gid, word)
