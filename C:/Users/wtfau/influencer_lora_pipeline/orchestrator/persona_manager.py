"""
Persona Manager - Load and manage persona configurations
"""
import os
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class ContentLane:
    name: str
    description: str
    vault_min: int
    vault_max: int
    vault_current: int = 0
    replenishment_threshold: int = 30
    platforms: List[str] = None
    llm: str = "claude"
    style: str = "natural"
    quality_tags: str = ""
    negative_prompt: str = ""

    def needs_replenishment(self):
        return self.vault_current < self.replenishment_threshold

    def get_example_prompt(self):
        return "A beautiful portrait"


@dataclass
class PersonaConfig:
    model_id: str
    model_name: str
    age: int
    heritage: str
    location: str
    niche: str
    height_cm: int
    build: str
    hair: str
    eyes: str
    skin: str
    personality_vibe: str
    personality_traits: List[str]
    hobbies: List[str]
    chat_tone: str
    chat_greetings: List[str]
    chat_preferred_topics: List[str]
    brand_aesthetic: str
    social_accounts: Dict[str, Any]
    monetization: Dict[str, Any]
    content_lanes: Dict[str, ContentLane]

    def get_lane(self, lane_name: str) -> Optional[ContentLane]:
        return self.content_lanes.get(lane_name)

    def get_lora_trigger_word(self, lane: str) -> str:
        return f"{self.model_id.lower()}_woman"


class PersonaManager:
    """Manages persona configurations"""

    def __init__(self, personas_dir: str = "./personas"):
        self.personas_dir = Path(personas_dir)
        self.personas: Dict[str, PersonaConfig] = {}
        self._load_personas()

    def _load_personas(self):
        """Load all persona configs from YAML files"""
        if not self.personas_dir.exists():
            print(f"Warning: Personas directory not found: {self.personas_dir}")
            return

        for persona_dir in self.personas_dir.iterdir():
            if persona_dir.is_dir():
                config_file = persona_dir / "persona_config.yaml"
                if config_file.exists():
                    try:
                        persona = self._load_persona_config(config_file)
                        self.personas[persona.model_id] = persona
                        print(f"Loaded persona: {persona.model_id} - {persona.model_name}")
                    except Exception as e:
                        print(f"Error loading {config_file}: {e}")

    def _load_persona_config(self, config_file: Path) -> PersonaConfig:
        """Load a single persona config from YAML"""
        with open(config_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        model_info = data.get('model_info', {})
        personality = data.get('personality', {})
        chat = data.get('chat', {})
        brand = data.get('brand', {})

        # Load content lanes
        lanes = {}
        for lane_name, lane_data in data.get('content_lanes', {}).items():
            vault = lane_data.get('vault', {})
            lanes[lane_name] = ContentLane(
                name=lane_name,
                description=lane_data.get('description', ''),
                vault_min=vault.get('min_images', 50),
                vault_max=vault.get('max_images', 200),
                vault_current=vault.get('current', 0),
                replenishment_threshold=vault.get('replenishment_threshold', 30),
                platforms=lane_data.get('platforms', []),
                llm=lane_data.get('llm', 'claude'),
                style=lane_data.get('style', 'natural'),
                quality_tags=lane_data.get('quality_tags', ''),
                negative_prompt=lane_data.get('negative_prompt', '')
            )

        return PersonaConfig(
            model_id=model_info.get('model_id', ''),
            model_name=model_info.get('model_name', ''),
            age=model_info.get('age', 25),
            heritage=model_info.get('heritage', ''),
            location=model_info.get('location', ''),
            niche=model_info.get('niche', ''),
            height_cm=model_info.get('height_cm', 170),
            build=model_info.get('build', ''),
            hair=model_info.get('hair', ''),
            eyes=model_info.get('eyes', ''),
            skin=model_info.get('skin', ''),
            personality_vibe=personality.get('vibe', ''),
            personality_traits=personality.get('traits', []),
            hobbies=personality.get('hobbies', []),
            chat_tone=chat.get('tone', 'friendly'),
            chat_greetings=chat.get('greetings', ['Hey!']),
            chat_preferred_topics=chat.get('preferred_topics', []),
            brand_aesthetic=brand.get('aesthetic', ''),
            social_accounts=data.get('social_accounts', {}),
            monetization=data.get('monetization', {}),
            content_lanes=lanes
        )

    def get_persona(self, model_id: str) -> Optional[PersonaConfig]:
        """Get a persona by ID"""
        return self.personas.get(model_id.upper())

    def get_all_personas(self) -> List[PersonaConfig]:
        """Get all loaded personas"""
        return list(self.personas.values())

    def check_replenishment_needed(self) -> List[tuple]:
        """Check which personas need replenishment"""
        needed = []
        for persona in self.personas.values():
            for lane_name, lane in persona.content_lanes.items():
                if lane.needs_replenishment():
                    needed.append((persona.model_id, lane_name))
        return needed
