from unittest.mock import Mock

from .crossclimb_parser import CrossClimbParser
from .crossclimb_solver import (
    CrossClimbSolver,
    DummyClassifier,
    ChatGPTClassifier,
)
import requests


def test_find_best_assignment():
    mock_parser = Mock(spec=CrossClimbParser)
    mock_parser.guess_elements = {0: None, 1: None}
    solver = CrossClimbSolver(mock_parser, DummyClassifier(["cat", "cot", "dog", "fog"]))
    candidates = {
        0: [("cat", 0.9), ("dog", 0.5)],
        1: [("cot", 0.8), ("fog", 0.6)],
    }
    result = solver.find_best_assignment(candidates)
    assert result == {0: "cat", 1: "cot"}


def test_chatgpt_classifier_parsing(monkeypatch):
    """Ensure the classifier correctly parses the API response."""
    fake_resp = Mock()
    fake_resp.json.return_value = [
        {"generated_text": "cat:0.9\ncot:0.8\n"}
    ]
    fake_resp.raise_for_status = Mock()
    monkeypatch.setattr(requests, "post", lambda *a, **k: fake_resp)

    clf = ChatGPTClassifier("dummy")
    result = clf.top_k("small feline", 3, 2)
    assert result == [("cat", 0.9), ("cot", 0.8)]
