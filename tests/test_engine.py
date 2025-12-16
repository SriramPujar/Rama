import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.engine import NarrativeEngine

class TestNarrativeEngine(unittest.TestCase):
    @patch('src.engine.LLMClient')
    def test_state_machine_flow(self, MockLLMClient):
        # Setup Mock
        mock_llm_instance = MockLLMClient.return_value
        mock_llm_instance.generate.side_effect = [
            "Stage 1 Output", "Stage 2 Output", "Stage 3 Output",
            "Stage 4 Output", "Stage 5 Output", "Stage 6 Output",
            "Next Situation Stage 1"
        ]

        engine = NarrativeEngine()
        
        # Initial State
        self.assertEqual(engine.stage, 0)
        self.assertEqual(engine.current_situation_id, 0)

        # Advance 1-6
        for i in range(1, 7):
            output = engine.advance()
            self.assertEqual(engine.stage, i)
            self.assertEqual(output, f"Stage {i} Output")
            self.assertIn(i, engine.stage_outputs)

        # Advance to next situation
        output = engine.advance()
        self.assertEqual(engine.stage, 1)
        self.assertEqual(engine.current_situation_id, 1)
        self.assertEqual(len(engine.history), 1)
        print("State machine flow verified successfully.")

if __name__ == '__main__':
    unittest.main()
