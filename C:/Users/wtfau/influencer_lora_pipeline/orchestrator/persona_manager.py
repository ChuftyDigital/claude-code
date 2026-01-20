"""
Persona Manager
===============
Loads and manages persona configurations from YAML files.
Provides easy access to persona data, content lanes, and generation settings.
"""

import os
import yaml
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ContentLane:
    """Represents a content lane (SFW, Spicy, or NSFW)"""
    name: str  # sfw, spicy, nsfw
    description: str
    platforms: List[str]

    # Vault configuration
    vault_min: int
    vault_max: int
    vault_current: int

    # Replenishment settings
    replenishment_threshold: int
    replenishment_batch_size: int
    auto_generate: bool

    # Prompt categories with weights
    prompt_categories: List[Dict[str, Any]]

    # Posting schedule
    posting_frequency: str
    posting_best_times: List[str]

    # Prompt enhancement settings
    llm: str
    style: str
    quality_tags: str
    negative_prompt: str

    def needs_replenishment(self) -> bool:
        """Check if vault needs replenishment"""
        return self.vault_current < self.replenishment_threshold

    def get_random_prompt_category(self) -> Dict[str, Any]:
        """Get a weighted random prompt category"""
        import random

        # Create weighted list
        weighted_categories = []
        for category in self.prompt_categories:
            weight = category.get("weight", 10)
            weighted_categories.extend([category] * weight)

        return random.choice(weighted_categories)

    def get_example_prompt(self) -> str:
        """Get a random example prompt from categories"""
        import random

        category = self.get_random_prompt_category()
        examples = category.get("examples", [])

        if not examples:
            return f"Portrait of {category.get('category', 'person')}"

        return random.choice(examples)


@dataclass
class PersonaConfig:
    """Complete persona configuration"""
    # Model basic info
    model_id: str
    model_name: str
    display_name: str
    age: int
    heritage: str
    location: str
    niche: str

    # Physical attributes
    height_cm: int
    build: str
    hair: str
    eyes: str
    skin: str
    features: List[str]

    # Personality
    personality_traits: List[str]
    personality_vibe: str
    hobbies: List[str]

    # Social media
    social_accounts: Dict[str, Dict[str, Any]]

    # Content lanes
    content_lanes: Dict[str, ContentLane]

    # LoRA training configs
    lora_training: Dict[str, Dict[str, Any]]

    # GHL tracking
    ghl_enabled: bool
    ghl_tags: List[str]

    # Monetization
    monetization: Dict[str, Any]

    # Chat personality
    chat_tone: str
    chat_greetings: List[str]
    chat_engagement_tactics: List[str]
    chat_preferred_topics: List[str]

    # Brand
    brand_colors: Dict[str, str]
    brand_aesthetic: str
    brand_hashtags_sfw: List[str]
    brand_hashtags_spicy: List[str]

    # Paths
    persona_dir: Path

    def get_lane(self, lane_name: str) -> Optional[ContentLane]:
        """Get a specific content lane"""
        return self.content_lanes.get(lane_name.lower())

    def get_vault_path(self, lane: str, subdir: str = "images") -> Path:
        """Get path to vault directory"""
        return self.persona_dir / lane.lower() / "vault" / subdir

    def get_training_path(self, lane: str, subdir: str = "images") -> Path:
        """Get path to training directory"""
        return self.persona_dir / lane.lower() / "training" / subdir

    def get_lora_trigger_word(self, lane: str) -> str:
        """Get the LoRA trigger word for a specific lane"""
        lora_config = self.lora_training.get(lane.lower(), {})
        return lora_config.get("trigger_word", f"{self.model_id}woman")


class PersonaManager:
    """
    Manages multiple personas and provides access to their configurations
    """

    def __init__(self, personas_dir: str = "./personas"):
        self.personas_dir = Path(personas_dir)
        self.personas: Dict[str, PersonaConfig] = {}
        self._load_all_personas()

    def _load_all_personas(self):
        """Load all persona configurations from the personas directory"""
        if not self.personas_dir.exists():
            logger.warning(f"Personas directory not found: {self.personas_dir}")
            return

        for persona_dir in self.personas_dir.iterdir():
            if persona_dir.is_dir():
                config_file = persona_dir / "persona_config.yaml"
                if config_file.exists():
                    try:
                        persona = self._load_persona_from_file(config_file, persona_dir)
                        if persona:
                            self.personas[persona.model_id] = persona
                            logger.info(f"Loaded persona: {persona.model_id} - {persona.model_name}")
                    except Exception as e:
                        logger.error(f"Error loading persona from {config_file}: {e}")

    def _load_persona_from_file(self, config_file: Path, persona_dir: Path) -> Optional[PersonaConfig]:
        """Load a single persona configuration from YAML file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            model_info = config.get("model_info", {})
            physical = model_info.get("physical", {})
            personality = model_info.get("personality", {})
            social = model_info.get("social", {})

            # Parse content lanes
            content_lanes = {}
            lanes_config = config.get("content_lanes", {})
            prompt_enhancement = config.get("prompt_enhancement", {})

            for lane_name in ["sfw", "spicy", "nsfw"]:
                lane_data = lanes_config.get(lane_name, {})
                if lane_data:
                    vault = lane_data.get("vault", {})
                    replenishment = lane_data.get("replenishment", {})
                    schedule = lane_data.get("posting_schedule", {})
                    enhancement = prompt_enhancement.get(lane_name, {})

                    content_lanes[lane_name] = ContentLane(
                        name=lane_name,
                        description=lane_data.get("description", ""),
                        platforms=lane_data.get("platforms", []),
                        vault_min=vault.get("min_images", 20),
                        vault_max=vault.get("max_images", 100),
                        vault_current=vault.get("current_count", 0),
                        replenishment_threshold=replenishment.get("threshold", 10),
                        replenishment_batch_size=replenishment.get("batch_size", 5),
                        auto_generate=replenishment.get("auto_generate", True),
                        prompt_categories=lane_data.get("prompt_categories", []),
                        posting_frequency=schedule.get("frequency", "daily"),
                        posting_best_times=schedule.get("best_times", []),
                        llm=enhancement.get("llm", "claude"),
                        style=enhancement.get("style", "professional"),
                        quality_tags=enhancement.get("quality_tags", "high quality"),
                        negative_prompt=enhancement.get("negative_prompt", "low quality, blurry")
                    )

            # Parse GHL tracking
            ghl_tracking = config.get("ghl_tracking", {})

            # Parse monetization
            monetization = config.get("monetization", {})

            # Parse chat personality
            chat_personality = config.get("chat_personality", {})

            # Parse brand
            brand = config.get("brand", {})

            # Parse LoRA training
            lora_training = config.get("lora_training", {})

            persona = PersonaConfig(
                model_id=model_info.get("model_id", "UNKNOWN"),
                model_name=model_info.get("model_name", "Unknown"),
                display_name=model_info.get("display_name", "Unknown"),
                age=model_info.get("age", 25),
                heritage=model_info.get("heritage", ""),
                location=model_info.get("location", ""),
                niche=model_info.get("niche", ""),
                height_cm=physical.get("height_cm", 170),
                build=physical.get("build", ""),
                hair=physical.get("hair", ""),
                eyes=physical.get("eyes", ""),
                skin=physical.get("skin", ""),
                features=physical.get("features", []),
                personality_traits=personality.get("traits", []),
                personality_vibe=personality.get("vibe", ""),
                hobbies=model_info.get("hobbies", []),
                social_accounts=social,
                content_lanes=content_lanes,
                lora_training=lora_training,
                ghl_enabled=ghl_tracking.get("enabled", False),
                ghl_tags=ghl_tracking.get("tags", []),
                monetization=monetization,
                chat_tone=chat_personality.get("tone", "friendly"),
                chat_greetings=chat_personality.get("greeting_messages", []),
                chat_engagement_tactics=chat_personality.get("engagement_tactics", []),
                chat_preferred_topics=chat_personality.get("preferred_topics", []),
                brand_colors=brand.get("colors", {}),
                brand_aesthetic=brand.get("aesthetic", ""),
                brand_hashtags_sfw=brand.get("hashtags_sfw", []),
                brand_hashtags_spicy=brand.get("hashtags_spicy", []),
                persona_dir=persona_dir
            )

            return persona

        except Exception as e:
            logger.error(f"Error parsing persona config: {e}")
            return None

    def get_persona(self, model_id: str) -> Optional[PersonaConfig]:
        """Get a persona by model ID"""
        return self.personas.get(model_id)

    def get_all_personas(self) -> List[PersonaConfig]:
        """Get all loaded personas"""
        return list(self.personas.values())

    def get_active_personas(self) -> List[PersonaConfig]:
        """Get all active personas (for now, all are active)"""
        return self.get_all_personas()

    def check_replenishment_needed(self) -> List[tuple[str, str]]:
        """
        Check all personas for lanes that need replenishment

        Returns:
            List of (model_id, lane_name) tuples that need replenishment
        """
        needs_replenishment = []

        for persona in self.personas.values():
            for lane_name, lane in persona.content_lanes.items():
                if lane.needs_replenishment():
                    needs_replenishment.append((persona.model_id, lane_name))

        return needs_replenishment

    def get_persona_summary(self, model_id: str) -> Dict[str, Any]:
        """Get a summary of persona info for display"""
        persona = self.get_persona(model_id)
        if not persona:
            return {}

        return {
            "model_id": persona.model_id,
            "name": persona.model_name,
            "niche": persona.niche,
            "location": persona.location,
            "content_lanes": {
                lane_name: {
                    "vault_count": lane.vault_current,
                    "needs_replenishment": lane.needs_replenishment(),
                    "platforms": lane.platforms
                }
                for lane_name, lane in persona.content_lanes.items()
            },
            "social_accounts": persona.social_accounts,
            "ghl_enabled": persona.ghl_enabled
        }


# Quick access functions
def load_persona(model_id: str, personas_dir: str = "./personas") -> Optional[PersonaConfig]:
    """Quick function to load a single persona"""
    manager = PersonaManager(personas_dir)
    return manager.get_persona(model_id)


def get_all_personas(personas_dir: str = "./personas") -> List[PersonaConfig]:
    """Quick function to get all personas"""
    manager = PersonaManager(personas_dir)
    return manager.get_all_personas()


# Example usage
if __name__ == "__main__":
    import json

    # Load all personas
    manager = PersonaManager("C:/Users/wtfau/influencer_lora_pipeline/personas")

    print("\n" + "=" * 60)
    print("LOADED PERSONAS")
    print("=" * 60)

    for persona in manager.get_all_personas():
        print(f"\n{persona.model_id}: {persona.model_name}")
        print(f"  Niche: {persona.niche}")
        print(f"  Location: {persona.location}")
        print(f"  Content Lanes:")

        for lane_name, lane in persona.content_lanes.items():
            print(f"    {lane_name.upper()}:")
            print(f"      Vault: {lane.vault_current}/{lane.vault_max}")
            print(f"      Needs Replenishment: {lane.needs_replenishment()}")
            print(f"      Platforms: {', '.join(lane.platforms)}")
            print(f"      LLM: {lane.llm}")

    # Check replenishment
    print("\n" + "=" * 60)
    print("REPLENISHMENT NEEDED")
    print("=" * 60)

    needs_replenishment = manager.check_replenishment_needed()
    if needs_replenishment:
        for model_id, lane_name in needs_replenishment:
            persona = manager.get_persona(model_id)
            lane = persona.get_lane(lane_name)
            print(f"\n{model_id} - {lane_name.upper()}")
            print(f"  Current: {lane.vault_current} | Threshold: {lane.replenishment_threshold}")
            print(f"  Batch Size: {lane.replenishment_batch_size}")
    else:
        print("\nAll vaults are stocked!")

    # Test getting a prompt example
    print("\n" + "=" * 60)
    print("EXAMPLE PROMPTS")
    print("=" * 60)

    for persona in manager.get_all_personas():
        print(f"\n{persona.model_name} ({persona.model_id}):")
        for lane_name in ["sfw", "spicy", "nsfw"]:
            lane = persona.get_lane(lane_name)
            if lane:
                example = lane.get_example_prompt()
                trigger = persona.get_lora_trigger_word(lane_name)
                print(f"\n  {lane_name.upper()}: {trigger}, {example}")
