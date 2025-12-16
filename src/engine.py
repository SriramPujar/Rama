from .llm_client import LLMClient
from .prompts import (
    SYSTEM_PROMPT,
    get_stage_1_prompt,
    get_stage_2_prompt,
    get_stage_3_prompt,
    get_stage_4_prompt,
    get_stage_5_prompt,
    get_stage_6_prompt
)

class NarrativeEngine:
    def __init__(self):
        self.llm = LLMClient()
        self.reset()

    def reset(self):
        self.current_situation_id = 0
        self.stage = 0
        self.history = [] # List of complete situations
        # Current situation buffers
        self.stage_outputs = {} 

    def advance(self):
        """Moves to the next stage and generates content."""
        self.stage += 1
        if self.stage > 6:
            # End of loop, commit to history and reset for next situation
            full_situation = "\n\n".join([f"### STAGE {k}\n{v}" for k,v in self.stage_outputs.items()])
            situation_header = f"\n\n## SITUATION {self.current_situation_id + 1}\n\n"
            
            # Persistence
            with open("generated_ramayana.md", "a", encoding="utf-8") as f:
                f.write(situation_header + full_situation + "\n\n---\n")
            
            self.history.append(full_situation)
            self.stage_outputs = {}
            self.stage = 1
            self.current_situation_id += 1
        
        return self._generate_current_stage()

    def _generate_current_stage(self):
        if self.stage == 1:
            # Pass recent history for continuity, but keep it brief
            context = self.history[-1] if self.history else None
            prompt = get_stage_1_prompt(context)
            output = self.llm.generate(SYSTEM_PROMPT, prompt, temperature=0.5)
        
        elif self.stage == 2:
            prompt = get_stage_2_prompt(self.stage_outputs[1])
            output = self.llm.generate(SYSTEM_PROMPT, prompt, temperature=0.1)

        elif self.stage == 3:
            prompt = get_stage_3_prompt(self.stage_outputs[1])
            output = self.llm.generate(SYSTEM_PROMPT, prompt, temperature=0.3)
        
        elif self.stage == 4:
            prompt = get_stage_4_prompt(self.stage_outputs[1], self.stage_outputs[3])
            output = self.llm.generate(SYSTEM_PROMPT, prompt, temperature=0.2)
        
        elif self.stage == 5:
            prompt = get_stage_5_prompt(self.stage_outputs[1], self.stage_outputs[4])
            output = self.llm.generate(SYSTEM_PROMPT, prompt, temperature=0.4)
        
        elif self.stage == 6:
            prompt = get_stage_6_prompt(
                self.stage_outputs[1], 
                self.stage_outputs[4], 
                self.stage_outputs[5]
            )
            output = self.llm.generate(SYSTEM_PROMPT, prompt, temperature=0.2)
        
        else:
            return "Error: Invalid Stage"

        self.stage_outputs[self.stage] = output
        return output

    def get_current_state(self):
        return {
            "situation_id": self.current_situation_id,
            "stage": self.stage,
            "content": self.stage_outputs
        }
