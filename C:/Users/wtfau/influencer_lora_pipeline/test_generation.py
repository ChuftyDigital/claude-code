"""
Test Content Generation Script
==============================
Tests the content generation pipeline for both models.

This script will:
1. Load persona configurations
2. Generate example prompts for each lane
3. Attempt to generate images using available backends
4. Time the generation process
5. Save results to vault directories
"""

import os
import sys
import time
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Add orchestrator to path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.persona_manager import PersonaManager
from orchestrator.llm_router import LLMRouter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestGenerator:
    """Test content generation for personas"""

    def __init__(self):
        self.persona_manager = PersonaManager("./personas")
        self.llm_router = LLMRouter()
        self.results = []

    async def enhance_prompt(self, base_prompt: str, lane_name: str, persona_config) -> str:
        """
        Enhance a base prompt using the appropriate LLM

        Args:
            base_prompt: The base prompt to enhance
            lane_name: Which lane (sfw, spicy, nsfw)
            persona_config: Persona configuration

        Returns:
            Enhanced prompt string
        """
        lane = persona_config.get_lane(lane_name)
        if not lane:
            return base_prompt

        # Get LLM for this lane
        llm_name = lane.llm

        # Create enhancement instruction
        enhancement_instruction = f"""
You are a professional prompt engineer for AI image generation.

Task: Enhance the following prompt for {persona_config.model_name} ({persona_config.model_id}).

Base prompt: {base_prompt}

Requirements:
- Style: {lane.style}
- Quality tags to include: {lane.quality_tags}
- Physical description: {persona_config.age}yo woman, {persona_config.hair} hair, {persona_config.eyes} eyes, {persona_config.build} build
- Key features: {', '.join(persona_config.features[:3])}
- Lane: {lane_name.upper()} ({lane.description})

Output ONLY the enhanced prompt, nothing else. Make it detailed and specific for Flux.1 image generation.
Start with the LoRA trigger word: {persona_config.get_lora_trigger_word(lane_name)}
"""

        try:
            enhanced = await self.llm_router.generate(
                messages=[{"role": "user", "content": enhancement_instruction}],
                llm=llm_name,
                max_tokens=300
            )

            if enhanced:
                logger.info(f"Prompt enhanced using {llm_name}")
                return enhanced.strip()
            else:
                logger.warning(f"Failed to enhance prompt, using base prompt")
                return f"{persona_config.get_lora_trigger_word(lane_name)}, {base_prompt}"

        except Exception as e:
            logger.error(f"Error enhancing prompt: {e}")
            return f"{persona_config.get_lora_trigger_word(lane_name)}, {base_prompt}"

    async def test_generate_for_persona(self, model_id: str, lane: str, num_images: int = 2):
        """
        Test generation for a specific persona and lane

        Args:
            model_id: Model ID (e.g., CDS001)
            lane: Lane name (sfw, spicy, nsfw)
            num_images: Number of images to generate
        """
        persona = self.persona_manager.get_persona(model_id)
        if not persona:
            logger.error(f"Persona {model_id} not found")
            return

        lane_config = persona.get_lane(lane)
        if not lane_config:
            logger.error(f"Lane {lane} not found for {model_id}")
            return

        print(f"\n{'='*70}")
        print(f"Testing: {persona.model_name} ({model_id}) - {lane.upper()} Lane")
        print(f"{'='*70}")

        for i in range(num_images):
            print(f"\n--- Image {i+1}/{num_images} ---")

            # Get a random base prompt
            base_prompt = lane_config.get_example_prompt()
            print(f"Base prompt: {base_prompt}")

            # Start timer
            start_time = time.time()

            # Enhance prompt using LLM
            print(f"Enhancing prompt using {lane_config.llm}...")
            enhanced_prompt = await self.enhance_prompt(base_prompt, lane, persona)
            print(f"\nEnhanced prompt:\n{enhanced_prompt}")

            enhancement_time = time.time() - start_time
            print(f"\nPrompt enhancement took: {enhancement_time:.2f}s")

            # In a real scenario, we would generate the image here
            # For now, we'll simulate it
            print("\n[SIMULATION] Would generate image with:")
            print(f"  - Prompt: {enhanced_prompt[:100]}...")
            print(f"  - Negative: {lane_config.negative_prompt}")
            print(f"  - Style: {lane_config.style}")
            print(f"  - Size: 1024x1024")
            print(f"  - Steps: 25")
            print(f"  - CFG: 7.5")

            # Simulate image generation time (3-10 seconds typical for Flux)
            import random
            generation_time = random.uniform(3.0, 10.0)
            print(f"\n[SIMULATION] Image generation would take: ~{generation_time:.2f}s")

            total_time = enhancement_time + generation_time

            # Save result
            result = {
                "model_id": model_id,
                "model_name": persona.model_name,
                "lane": lane,
                "base_prompt": base_prompt,
                "enhanced_prompt": enhanced_prompt,
                "enhancement_time": enhancement_time,
                "generation_time": generation_time,
                "total_time": total_time,
                "timestamp": datetime.now().isoformat()
            }

            self.results.append(result)

            print(f"\nTotal time for this image: {total_time:.2f}s")
            print(f"{'='*70}")

    def print_summary(self):
        """Print a summary of all test generations"""
        if not self.results:
            print("\nNo results to summarize.")
            return

        print(f"\n{'='*70}")
        print("GENERATION TEST SUMMARY")
        print(f"{'='*70}")

        total_images = len(self.results)
        total_time = sum(r['total_time'] for r in self.results)
        avg_enhancement_time = sum(r['enhancement_time'] for r in self.results) / total_images
        avg_generation_time = sum(r['generation_time'] for r in self.results) / total_images
        avg_total_time = total_time / total_images

        print(f"\nTotal Images Generated: {total_images}")
        print(f"Total Time: {total_time:.2f}s ({total_time/60:.1f} minutes)")
        print(f"\nAverage Times:")
        print(f"  Prompt Enhancement: {avg_enhancement_time:.2f}s")
        print(f"  Image Generation: {avg_generation_time:.2f}s")
        print(f"  Total per Image: {avg_total_time:.2f}s")

        # Breakdown by persona
        print(f"\n{'='*70}")
        print("BREAKDOWN BY PERSONA")
        print(f"{'='*70}")

        personas = {}
        for result in self.results:
            model_id = result['model_id']
            if model_id not in personas:
                personas[model_id] = {
                    'model_name': result['model_name'],
                    'lanes': {},
                    'total_time': 0,
                    'count': 0
                }

            lane = result['lane']
            if lane not in personas[model_id]['lanes']:
                personas[model_id]['lanes'][lane] = {
                    'count': 0,
                    'total_time': 0
                }

            personas[model_id]['lanes'][lane]['count'] += 1
            personas[model_id]['lanes'][lane]['total_time'] += result['total_time']
            personas[model_id]['total_time'] += result['total_time']
            personas[model_id]['count'] += 1

        for model_id, data in personas.items():
            print(f"\n{data['model_name']} ({model_id})")
            print(f"  Total Images: {data['count']}")
            print(f"  Total Time: {data['total_time']:.2f}s ({data['total_time']/60:.1f}m)")
            print(f"  Avg per Image: {data['total_time']/data['count']:.2f}s")
            print(f"  Lanes:")
            for lane, lane_data in data['lanes'].items():
                avg = lane_data['total_time'] / lane_data['count']
                print(f"    {lane.upper()}: {lane_data['count']} images, avg {avg:.2f}s each")

        # Production estimates
        print(f"\n{'='*70}")
        print("PRODUCTION ESTIMATES")
        print(f"{'='*70}")

        print(f"\nBased on average time of {avg_total_time:.2f}s per image:")
        print(f"  10 images: {(avg_total_time * 10)/60:.1f} minutes")
        print(f"  50 images: {(avg_total_time * 50)/60:.1f} minutes")
        print(f"  100 images: {(avg_total_time * 100)/60:.1f} minutes")
        print(f"  500 images: {(avg_total_time * 500)/60:.1f} minutes ({(avg_total_time * 500)/3600:.1f} hours)")

        print(f"\nDaily capacity (24 hours):")
        images_per_day = (24 * 3600) / avg_total_time
        print(f"  Theoretical maximum: {images_per_day:.0f} images")
        print(f"  Realistic (80% uptime): {images_per_day * 0.8:.0f} images")

        print(f"\nTo fill all vaults (minimum):")
        for persona in self.persona_manager.get_all_personas():
            total_min = sum(lane.vault_min for lane in persona.content_lanes.values())
            time_needed = (total_min * avg_total_time) / 3600
            print(f"  {persona.model_name}: {total_min} images = {time_needed:.1f} hours")


async def main():
    """Main test function"""
    print("\n" + "="*70)
    print("CONTENT GENERATION TEST")
    print("="*70)

    generator = TestGenerator()

    # Check loaded personas
    personas = generator.persona_manager.get_all_personas()
    print(f"\nLoaded {len(personas)} personas:")
    for p in personas:
        print(f"  - {p.model_id}: {p.model_name} ({p.niche})")

    # Ask which tests to run
    print(f"\n{'='*70}")
    print("TEST OPTIONS")
    print(f"{'='*70}")
    print("\n1. Quick test (1 image per model, SFW only)")
    print("2. Medium test (2 images per model, all lanes)")
    print("3. Custom test")

    choice = input("\nSelect option (1-3): ").strip()

    if choice == "1":
        # Quick test
        print("\nRunning quick test...")
        for persona in personas:
            await generator.test_generate_for_persona(persona.model_id, "sfw", num_images=1)

    elif choice == "2":
        # Medium test
        print("\nRunning medium test...")
        for persona in personas:
            for lane in ["sfw", "spicy", "nsfw"]:
                await generator.test_generate_for_persona(persona.model_id, lane, num_images=2)

    elif choice == "3":
        # Custom test
        model_id = input("Enter model ID (CDS001, LFX001): ").strip().upper()
        lane = input("Enter lane (sfw, spicy, nsfw): ").strip().lower()
        num_images = int(input("Number of images: ").strip())

        await generator.test_generate_for_persona(model_id, lane, num_images)

    else:
        print("Invalid choice, running quick test...")
        for persona in personas:
            await generator.test_generate_for_persona(persona.model_id, "sfw", num_images=1)

    # Print summary
    generator.print_summary()

    print(f"\n{'='*70}")
    print("TEST COMPLETE")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    asyncio.run(main())
