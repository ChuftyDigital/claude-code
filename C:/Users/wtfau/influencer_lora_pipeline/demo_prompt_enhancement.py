"""
Prompt Enhancement Demo
======================
Demonstrates prompt enhancement for content generation without actually generating images.
Shows what the prompts would look like and estimates generation timeframes.
"""

import sys
import asyncio
import time
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.persona_manager import PersonaManager
from orchestrator.llm_router import LLMRouter

load_dotenv()


async def demo():
    """Run the demo"""
    print("\n" + "="*80)
    print("CONTENT GENERATION PROMPT ENHANCEMENT DEMO")
    print("="*80)

    # Load personas
    manager = PersonaManager("./personas")
    personas = manager.get_all_personas()

    print(f"\nLoaded {len(personas)} personas:")
    for p in personas:
        print(f"  • {p.model_id}: {p.model_name} - {p.niche}")

    # Initialize LLM router
    llm_router = LLMRouter()

    # Demo for CDS001 (Cristie)
    print("\n" + "="*80)
    print("MODEL 1: CRISTIE DESOUZA (CDS001) - Beach Lifestyle")
    print("="*80)

    cristie = manager.get_persona("CDS001")
    if cristie:
        for lane_name in ["sfw", "spicy"]:
            lane = cristie.get_lane(lane_name)
            print(f"\n{'-'*80}")
            print(f"{lane_name.upper()} LANE - {lane.description}")
            print(f"{'-'*80}")

            # Get example base prompt
            base_prompt = lane.get_example_prompt()
            print(f"\nBase Prompt:\n  {base_prompt}")

            # Show trigger word
            trigger = cristie.get_lora_trigger_word(lane_name)
            print(f"\nLoRA Trigger Word: {trigger}")

            # Create enhancement instruction
            enhancement_instruction = f"""You are a professional prompt engineer for AI image generation.

Task: Enhance this prompt for {cristie.model_name}, a {cristie.age}yo Brazilian beach lifestyle model.

Base prompt: {base_prompt}

Physical description:
- Hair: {cristie.hair}
- Eyes: {cristie.eyes}
- Build: {cristie.build}
- Skin: {cristie.skin}
- Features: {', '.join(cristie.features)}

Style requirements: {lane.style}
Quality tags: {lane.quality_tags}

Output ONLY the enhanced prompt starting with "{trigger}". Make it detailed for Flux.1."""

            print(f"\nEnhancing with {lane.llm.upper()}...")
            start_time = time.time()

            try:
                enhanced = await llm_router.generate(
                    messages=[{"role": "user", "content": enhancement_instruction}],
                    llm=lane.llm,
                    max_tokens=300
                )

                enhancement_time = time.time() - start_time

                if enhanced:
                    print(f"\nEnhanced Prompt ({enhancement_time:.2f}s):")
                    print(f"  {enhanced.strip()}")
                else:
                    print("\n  [Enhancement failed, would use base prompt]")

            except Exception as e:
                print(f"\n  [Error: {e}]")

            print(f"\nNegative Prompt:\n  {lane.negative_prompt}")

    # Demo for LFX001 (Lexi)
    print("\n" + "="*80)
    print("MODEL 2: LEXI FAIRFAX (LFX001) - Equestrian / High Society")
    print("="*80)

    lexi = manager.get_persona("LFX001")
    if lexi:
        for lane_name in ["sfw", "spicy"]:
            lane = lexi.get_lane(lane_name)
            print(f"\n{'-'*80}")
            print(f"{lane_name.upper()} LANE - {lane.description}")
            print(f"{'-'*80}")

            # Get example base prompt
            base_prompt = lane.get_example_prompt()
            print(f"\nBase Prompt:\n  {base_prompt}")

            # Show trigger word
            trigger = lexi.get_lora_trigger_word(lane_name)
            print(f"\nLoRA Trigger Word: {trigger}")

            # Create enhancement instruction
            enhancement_instruction = f"""You are a professional prompt engineer for AI image generation.

Task: Enhance this prompt for {lexi.model_name}, a {lexi.age}yo sophisticated British aristocrat.

Base prompt: {base_prompt}

Physical description:
- Hair: {lexi.hair}
- Eyes: {lexi.eyes}
- Build: {lexi.build}
- Skin: {lexi.skin}
- Features: {', '.join(lexi.features)}

Style requirements: {lane.style}
Quality tags: {lane.quality_tags}

Output ONLY the enhanced prompt starting with "{trigger}". Make it detailed for Flux.1."""

            print(f"\nEnhancing with {lane.llm.upper()}...")
            start_time = time.time()

            try:
                enhanced = await llm_router.generate(
                    messages=[{"role": "user", "content": enhancement_instruction}],
                    llm=lane.llm,
                    max_tokens=300
                )

                enhancement_time = time.time() - start_time

                if enhanced:
                    print(f"\nEnhanced Prompt ({enhancement_time:.2f}s):")
                    print(f"  {enhanced.strip()}")
                else:
                    print("\n  [Enhancement failed, would use base prompt]")

            except Exception as e:
                print(f"\n  [Error: {e}]")

            print(f"\nNegative Prompt:\n  {lane.negative_prompt}")

    # Generation time estimates
    print("\n" + "="*80)
    print("TIMEFRAME ESTIMATES")
    print("="*80)

    print("""
Based on typical Flux.1 generation with these specifications:
  • Image size: 1024x1024
  • Steps: 25
  • Guidance scale: 7.5
  • Hardware: RTX 4090 / A100

Per Image Breakdown:
  • Prompt enhancement (LLM): 1-3 seconds
  • Image generation (Flux.1): 3-10 seconds
  • Post-processing & save: 0.5-1 seconds
  ──────────────────────────────────────
  • TOTAL PER IMAGE: ~5-14 seconds average

Batch Generation Estimates:
  • 10 images:  ~1-2 minutes
  • 50 images:  ~5-12 minutes
  • 100 images: ~10-25 minutes
  • 500 images: ~45-120 minutes (0.75-2 hours)

Initial Vault Setup (per model):
  • SFW lane (50 images):    ~5-12 minutes
  • Spicy lane (40 images):  ~4-10 minutes
  • NSFW lane (30 images):   ~3-7 minutes
  ──────────────────────────────────────
  • TOTAL PER MODEL: ~12-30 minutes

For both models (CDS001 + LFX001):
  • Total images needed: 240 images
  • Estimated time: ~25-60 minutes

Daily Production Capacity (24/7 generation):
  • Conservative estimate: ~3,000-5,000 images/day
  • With 80% uptime: ~2,400-4,000 images/day

Recommended Workflow:
  1. Generate initial vault stock: ~1 hour for both models
  2. Set up replenishment automation
  3. Auto-generate when vault < threshold
  4. Monitor and adjust based on posting schedule

Quality Optimization:
  • Use batch generation for efficiency
  • Queue prompts during off-peak hours
  • Implement A/B testing for prompt styles
  • Track engagement metrics per content type
""")

    print("="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print("\nNext Steps:")
    print("  1. Start ComfyUI/A1111 backend")
    print("  2. Run actual image generation test")
    print("  3. Review and refine prompts based on results")
    print("  4. Set up automation for scheduled generation")
    print("  5. Integrate with social media platforms")
    print()


if __name__ == "__main__":
    asyncio.run(demo())
