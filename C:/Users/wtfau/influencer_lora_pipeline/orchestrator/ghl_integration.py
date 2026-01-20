"""
Go High Level Integration Module
=================================
Tracks model performance, earnings, and customer interactions in GHL CRM.

This module provides:
1. Model tracking - Store model data, content stats, earnings
2. Customer tracking - Record all customer interactions across models
3. Interaction logging - Detailed conversation and transaction history
4. Revenue attribution - Link purchases to specific content/interactions
5. Personalization data - Build customer profiles for targeted engagement

GHL API Documentation: https://highlevel.stoplight.io/
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import aiohttp
import json

logger = logging.getLogger(__name__)


@dataclass
class ModelRecord:
    """Model information stored in GHL"""
    model_id: str  # e.g., CDS001
    model_name: str  # e.g., Cristie Desouza
    niche: str
    age: int
    location: str
    status: str  # active, paused, archived

    # Performance metrics
    total_content_generated: int = 0
    total_earnings: float = 0.0
    total_interactions: int = 0
    total_customers: int = 0

    # Platform stats
    instagram_followers: int = 0
    twitter_followers: int = 0
    onlyfans_subscribers: int = 0
    fansly_subscribers: int = 0

    # Dates
    created_at: str = ""
    last_content_generated: str = ""
    last_interaction: str = ""

    def to_ghl_contact(self) -> Dict[str, Any]:
        """Convert to GHL contact format"""
        return {
            "firstName": self.model_name.split()[0],
            "lastName": " ".join(self.model_name.split()[1:]) if len(self.model_name.split()) > 1 else "",
            "email": f"{self.model_id.lower()}@production.studio",
            "phone": "",
            "tags": ["AI Model", f"Niche:{self.niche}", f"Status:{self.status}"],
            "customFields": {
                "model_id": self.model_id,
                "model_niche": self.niche,
                "model_age": str(self.age),
                "model_location": self.location,
                "total_content": str(self.total_content_generated),
                "total_earnings": f"${self.total_earnings:.2f}",
                "total_interactions": str(self.total_interactions),
                "total_customers": str(self.total_customers),
                "created_at": self.created_at,
                "last_content": self.last_content_generated,
                "last_interaction": self.last_interaction
            }
        }


@dataclass
class CustomerRecord:
    """Customer information stored in GHL"""
    customer_id: str  # Unique ID (from platform)
    platform: str  # instagram, twitter, onlyfans, fansly
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None

    # Interaction history
    models_interacted_with: List[str] = None  # List of model IDs
    total_interactions: int = 0
    total_purchases: float = 0.0
    average_purchase: float = 0.0

    # Preferences (learned from interactions)
    preferred_content_types: List[str] = None  # e.g., ["beach", "fitness", "bikini"]
    preferred_niches: List[str] = None
    interaction_times: List[str] = None  # Best times to engage

    # Engagement level
    engagement_score: int = 0  # 0-100
    last_interaction: str = ""
    first_interaction: str = ""
    status: str = "active"  # active, inactive, vip, blocked

    def __post_init__(self):
        if self.models_interacted_with is None:
            self.models_interacted_with = []
        if self.preferred_content_types is None:
            self.preferred_content_types = []
        if self.preferred_niches is None:
            self.preferred_niches = []
        if self.interaction_times is None:
            self.interaction_times = []

    def to_ghl_contact(self) -> Dict[str, Any]:
        """Convert to GHL contact format"""
        return {
            "firstName": self.username,
            "lastName": f"({self.platform})",
            "email": self.email or f"{self.customer_id}@placeholder.com",
            "phone": self.phone or "",
            "tags": [
                "Customer",
                f"Platform:{self.platform}",
                f"Status:{self.status}",
                f"Engagement:{self.engagement_score}"
            ] + [f"Model:{m}" for m in self.models_interacted_with],
            "customFields": {
                "customer_id": self.customer_id,
                "platform": self.platform,
                "username": self.username,
                "total_interactions": str(self.total_interactions),
                "total_purchases": f"${self.total_purchases:.2f}",
                "average_purchase": f"${self.average_purchase:.2f}",
                "engagement_score": str(self.engagement_score),
                "models_interacted": ",".join(self.models_interacted_with),
                "preferred_content": ",".join(self.preferred_content_types),
                "preferred_niches": ",".join(self.preferred_niches),
                "first_interaction": self.first_interaction,
                "last_interaction": self.last_interaction
            }
        }


@dataclass
class InteractionRecord:
    """Single interaction between customer and model"""
    interaction_id: str
    timestamp: str
    model_id: str
    customer_id: str
    platform: str
    interaction_type: str  # message, purchase, like, comment, tip

    # Details
    content_type: Optional[str] = None  # What content triggered this
    message_content: Optional[str] = None  # If it's a message
    purchase_amount: float = 0.0

    # Context for personalization
    customer_sentiment: str = "neutral"  # positive, neutral, negative
    topics_discussed: List[str] = None

    def __post_init__(self):
        if self.topics_discussed is None:
            self.topics_discussed = []

    def to_ghl_note(self) -> str:
        """Convert to GHL note format"""
        note = f"[{self.timestamp}] {self.interaction_type.upper()} on {self.platform}\n"
        note += f"Model: {self.model_id} | Customer: {self.customer_id}\n"

        if self.content_type:
            note += f"Content Type: {self.content_type}\n"
        if self.purchase_amount > 0:
            note += f"Purchase: ${self.purchase_amount:.2f}\n"
        if self.message_content:
            note += f"Message: {self.message_content[:200]}...\n"
        if self.topics_discussed:
            note += f"Topics: {', '.join(self.topics_discussed)}\n"

        note += f"Sentiment: {self.customer_sentiment}"
        return note


class GHLClient:
    """
    Go High Level API Client
    Handles all communication with GHL CRM
    """

    def __init__(self, api_key: str, location_id: str):
        """
        Initialize GHL client

        Args:
            api_key: GHL API key (from agency settings)
            location_id: GHL location ID (your sub-account)
        """
        self.api_key = api_key
        self.location_id = location_id
        self.base_url = "https://rest.gohighlevel.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def create_or_update_contact(self, contact_data: Dict[str, Any]) -> Optional[str]:
        """
        Create or update a contact in GHL

        Args:
            contact_data: Contact information in GHL format

        Returns:
            Contact ID if successful, None otherwise
        """
        try:
            # First, search for existing contact by email
            email = contact_data.get("email")
            existing_contact = await self.find_contact_by_email(email)

            if existing_contact:
                # Update existing
                contact_id = existing_contact["id"]
                url = f"{self.base_url}/contacts/{contact_id}"
                async with self.session.put(url, json=contact_data) as resp:
                    if resp.status == 200:
                        logger.info(f"Updated contact: {email}")
                        return contact_id
                    else:
                        logger.error(f"Failed to update contact: {await resp.text()}")
                        return None
            else:
                # Create new
                contact_data["locationId"] = self.location_id
                url = f"{self.base_url}/contacts"
                async with self.session.post(url, json=contact_data) as resp:
                    if resp.status == 201:
                        result = await resp.json()
                        contact_id = result.get("contact", {}).get("id")
                        logger.info(f"Created contact: {email}")
                        return contact_id
                    else:
                        logger.error(f"Failed to create contact: {await resp.text()}")
                        return None

        except Exception as e:
            logger.error(f"Error creating/updating contact: {e}")
            return None

    async def find_contact_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find contact by email address"""
        try:
            url = f"{self.base_url}/contacts/lookup"
            params = {"email": email, "locationId": self.location_id}

            async with self.session.get(url, params=params) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    contacts = result.get("contacts", [])
                    return contacts[0] if contacts else None
                return None

        except Exception as e:
            logger.error(f"Error finding contact: {e}")
            return None

    async def add_note_to_contact(self, contact_id: str, note: str) -> bool:
        """Add a note to a contact (for interaction logging)"""
        try:
            url = f"{self.base_url}/contacts/{contact_id}/notes"
            data = {
                "body": note,
                "locationId": self.location_id
            }

            async with self.session.post(url, json=data) as resp:
                if resp.status == 201:
                    logger.info(f"Added note to contact {contact_id}")
                    return True
                else:
                    logger.error(f"Failed to add note: {await resp.text()}")
                    return False

        except Exception as e:
            logger.error(f"Error adding note: {e}")
            return False

    async def add_tag_to_contact(self, contact_id: str, tag: str) -> bool:
        """Add a tag to a contact"""
        try:
            url = f"{self.base_url}/contacts/{contact_id}/tags"
            data = {"tags": [tag]}

            async with self.session.post(url, json=data) as resp:
                if resp.status == 200:
                    logger.info(f"Added tag '{tag}' to contact {contact_id}")
                    return True
                else:
                    logger.error(f"Failed to add tag: {await resp.text()}")
                    return False

        except Exception as e:
            logger.error(f"Error adding tag: {e}")
            return False

    async def update_custom_field(self, contact_id: str, field_key: str, value: str) -> bool:
        """Update a single custom field"""
        try:
            url = f"{self.base_url}/contacts/{contact_id}"
            data = {
                "customFields": {
                    field_key: value
                }
            }

            async with self.session.put(url, json=data) as resp:
                if resp.status == 200:
                    return True
                return False

        except Exception as e:
            logger.error(f"Error updating custom field: {e}")
            return False


class GHLDataManager:
    """
    Proactive Data Management Agent
    Monitors and syncs all model and customer data to GHL
    """

    def __init__(self, api_key: str, location_id: str):
        self.client = GHLClient(api_key, location_id)
        self.model_cache: Dict[str, str] = {}  # model_id -> ghl_contact_id
        self.customer_cache: Dict[str, str] = {}  # customer_id -> ghl_contact_id

    async def sync_model(self, model: ModelRecord) -> bool:
        """Sync model data to GHL"""
        async with self.client as ghl:
            contact_data = model.to_ghl_contact()
            contact_id = await ghl.create_or_update_contact(contact_data)

            if contact_id:
                self.model_cache[model.model_id] = contact_id
                logger.info(f"Synced model {model.model_id} to GHL")
                return True
            return False

    async def sync_customer(self, customer: CustomerRecord) -> bool:
        """Sync customer data to GHL"""
        async with self.client as ghl:
            contact_data = customer.to_ghl_contact()
            contact_id = await ghl.create_or_update_contact(contact_data)

            if contact_id:
                self.customer_cache[customer.customer_id] = contact_id
                logger.info(f"Synced customer {customer.customer_id} to GHL")
                return True
            return False

    async def log_interaction(self, interaction: InteractionRecord) -> bool:
        """Log an interaction to both model and customer records"""
        async with self.client as ghl:
            # Add note to customer contact
            customer_ghl_id = self.customer_cache.get(interaction.customer_id)
            if customer_ghl_id:
                note = interaction.to_ghl_note()
                await ghl.add_note_to_contact(customer_ghl_id, note)

            # Update model stats
            model_ghl_id = self.model_cache.get(interaction.model_id)
            if model_ghl_id:
                # Increment interaction count
                pass  # Would need to fetch current value, increment, update

            logger.info(f"Logged interaction: {interaction.interaction_id}")
            return True

    async def update_model_earnings(self, model_id: str, amount: float) -> bool:
        """Update model's total earnings"""
        async with self.client as ghl:
            model_ghl_id = self.model_cache.get(model_id)
            if not model_ghl_id:
                logger.warning(f"Model {model_id} not found in cache")
                return False

            # This would need to fetch current earnings, add amount, update
            # For now, just log it
            logger.info(f"Model {model_id} earned ${amount:.2f}")
            return True

    async def update_customer_purchase(self, customer_id: str, amount: float,
                                       model_id: str, content_type: str) -> bool:
        """Record a customer purchase"""
        # Log the purchase
        interaction = InteractionRecord(
            interaction_id=f"purchase_{datetime.now().timestamp()}",
            timestamp=datetime.now().isoformat(),
            model_id=model_id,
            customer_id=customer_id,
            platform="onlyfans",  # or detect from context
            interaction_type="purchase",
            content_type=content_type,
            purchase_amount=amount,
            customer_sentiment="positive"
        )

        await self.log_interaction(interaction)
        await self.update_model_earnings(model_id, amount)

        return True

    async def get_customer_preferences(self, customer_id: str) -> Optional[CustomerRecord]:
        """
        Retrieve customer preferences for personalized chat
        This would be called by the chat agent before responding
        """
        # In real implementation, would fetch from GHL and reconstruct CustomerRecord
        # For now, return None
        logger.info(f"Fetching preferences for customer {customer_id}")
        return None

    async def update_customer_preferences(self, customer_id: str,
                                         new_preferences: Dict[str, Any]) -> bool:
        """
        Update customer preferences based on chat interactions
        Called by chat agent after learning new information
        """
        async with self.client as ghl:
            customer_ghl_id = self.customer_cache.get(customer_id)
            if not customer_ghl_id:
                return False

            # Update custom fields with new preferences
            for key, value in new_preferences.items():
                await ghl.update_custom_field(customer_ghl_id, key, str(value))

            logger.info(f"Updated preferences for customer {customer_id}")
            return True


# Integration hooks for the orchestrator
async def on_content_generated(model_id: str, content_type: str,
                               ghl_manager: GHLDataManager):
    """Called after content is generated"""
    # Update model's content count
    logger.info(f"Content generated: {model_id} - {content_type}")
    # Would update GHL here


async def on_customer_interaction(model_id: str, customer_id: str,
                                  platform: str, message: str,
                                  ghl_manager: GHLDataManager):
    """Called when customer interacts with model"""
    interaction = InteractionRecord(
        interaction_id=f"msg_{datetime.now().timestamp()}",
        timestamp=datetime.now().isoformat(),
        model_id=model_id,
        customer_id=customer_id,
        platform=platform,
        interaction_type="message",
        message_content=message
    )

    await ghl_manager.log_interaction(interaction)


async def on_customer_purchase(model_id: str, customer_id: str,
                               amount: float, content_type: str,
                               ghl_manager: GHLDataManager):
    """Called when customer makes a purchase"""
    await ghl_manager.update_customer_purchase(
        customer_id=customer_id,
        amount=amount,
        model_id=model_id,
        content_type=content_type
    )


# Example usage
if __name__ == "__main__":
    import asyncio

    async def main():
        # Initialize manager
        api_key = os.getenv("GHL_API_KEY", "")
        location_id = os.getenv("GHL_LOCATION_ID", "")

        if not api_key or not location_id:
            print("Please set GHL_API_KEY and GHL_LOCATION_ID in .env")
            return

        manager = GHLDataManager(api_key, location_id)

        # Example: Sync a model
        cristie = ModelRecord(
            model_id="CDS001",
            model_name="Cristie Desouza",
            niche="Beach Lifestyle",
            age=27,
            location="Brazil/Miami",
            status="active",
            created_at=datetime.now().isoformat()
        )

        await manager.sync_model(cristie)

        # Example: Sync a customer
        customer = CustomerRecord(
            customer_id="ig_john123",
            platform="instagram",
            username="john123",
            email="john@example.com",
            first_interaction=datetime.now().isoformat()
        )

        await manager.sync_customer(customer)

        # Example: Log interaction
        interaction = InteractionRecord(
            interaction_id="int_001",
            timestamp=datetime.now().isoformat(),
            model_id="CDS001",
            customer_id="ig_john123",
            platform="instagram",
            interaction_type="message",
            message_content="Hey! Love your beach content!",
            customer_sentiment="positive",
            topics_discussed=["beach", "lifestyle"]
        )

        await manager.log_interaction(interaction)

        print("GHL sync completed!")

    asyncio.run(main())
