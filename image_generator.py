import torch
from diffusers import DiffusionPipeline, LCMScheduler
#https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
class ImageGenerator:
    def __init__(self, model_name: str="stabilityai/stable-diffusion-xl-base-1.0", device: str="cuda"):
        if device.lower() == "cuda":
            self.dtype=torch.float16
            self.variant="fp16"
        else:
            self.dtype=torch.float32
            self.variant="fp32"
            
        self.pipe = DiffusionPipeline.from_pretrained(
                            model_name,
                            variant=self.variant,
                            torch_dtype=self.dtype
                            ).to(device)
        self.pipe.scheduler = LCMScheduler.from_config(self.pipe.scheduler.config)
        # load LoRAs
        self.pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl", adapter_name="lcm")
        self.pipe.load_lora_weights("TheLastBen/Papercut_SDXL", weight_name="papercut.safetensors", adapter_name="papercut")
        # Combine LoRAs
        self.pipe.set_adapters(["lcm", "papercut"], adapter_weights=[1.0, 0.8])
    
    def generate(self, prompt: str):
        image = self.pipe(prompt, num_inference_steps=4, guidance_scale=1).images[0]
        return image