from PIL import Image
import io
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
#https://huggingface.co/timbrooks/instruct-pix2pix
class Image2Image:
    def __init__(self, img, model_id="timbrooks/instruct-pix2pix"):
        self.img = img
        self.pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
            model_id, torch_dtype=torch.float16, safety_checker=None).to("cuda")
        self.pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(self.pipe.scheduler.config)
    
    def generate(self, prompt: str):
        if not isinstance(self.img, Image.Image):
            try:
                # Open the image using PIL
                pil_image = Image.open(io.BytesIO(self.img.read()))
            except Exception as e:
                raise ValueError("Failed to open the image.") from e
        else:
            pil_image = self.img

        images = self.pipe(prompt, image=pil_image,
                           num_inference_steps=10, image_guidance_scale=1).images
        return images[0]