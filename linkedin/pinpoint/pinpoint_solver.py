import os
import time
import openai
from pinpoint_parser import PinpointParser


class PinpointSolver:
    def __init__(self, parser: PinpointParser):
        self.parser = parser
        self.clues = self.parser.dump_clues()

    def ask_llm(self) -> str:
        visible_clues = [c for c in self.clues if c]
        prompt = (
            "Given the following clue words: " + ", ".join(visible_clues) +
            ". Guess a single word that relates to all of them."
        )
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        guess = response.choices[0].message.content.strip().split()[0]
        return guess

    def solve(self):
        while self.clues.count(None) > 0:
            guess = self.ask_llm()
            self.parser.submit_guess(guess)
            time.sleep(1)
            self.clues = self.parser.dump_clues()
        print("All clues revealed!")
        final_guess = self.ask_llm()
        self.parser.submit_guess(final_guess)
        print("Final guess:", final_guess)


if __name__ == '__main__':
    parser = PinpointParser()
    solver = PinpointSolver(parser)
    solver.solve()
