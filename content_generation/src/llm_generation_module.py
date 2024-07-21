import dspy
from src.signatures import VoiceOverSignature, VideoGenScriptSignature


class GenerationModule(dspy.Module):
    def __init__(self, llm):
        super().__init__()
        self.llm = llm
        self.voice_over_signature = dspy.ChainOfThought(VoiceOverSignature)
        self.video_gen_script_signature = dspy.ChainOfThought(VideoGenScriptSignature)

    def forward(self, parsed_paper_data):
        with dspy.context(lm=self.llm):
            voice_over = self.voice_over_signature(parsed_paper_data=parsed_paper_data).voice_over_script
            video_script = self.video_gen_script_signature(parsed_paper_data=parsed_paper_data,
                                                           voice_over_script=voice_over).video_flow_script

        return {'voice_over_script': voice_over, 'video_script': video_script}
