"""
LLM Router
==========
Routes prompt enhancement requests to different LLM providers.

Supports:
- Claude (Anthropic) - for SFW content
- Grok (xAI) - for Spicy/NSFW content
- ChatGPT (OpenAI) - alternative
- Ollama - local option
"""

import os
import logging
from typing import List, Dict, Optional, Any
import aiohttp
import anthropic
import openai

logger = logging.getLogger(__name__)


class LLMRouter:
    """Routes LLM requests to appropriate providers"""

    def __init__(self):
        # API keys from environment
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.xai_key = os.getenv("XAI_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        # Initialize clients
        if self.anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
        else:
            self.anthropic_client = None

        if self.openai_key:
            self.openai_client = openai.OpenAI(api_key=self.openai_key)
        else:
            self.openai_client = None

    async def generate(
        self,
        messages: List[Dict[str, str]],
        llm: str = "claude",
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Generate text using specified LLM

        Args:
            messages: List of message dicts with 'role' and 'content'
            llm: Which LLM to use ('claude', 'grok', 'chatgpt', 'ollama')
            max_tokens: Maximum tokens to generate
            temperature: Generation temperature

        Returns:
            Generated text or None if failed
        """
        llm = llm.lower()

        try:
            if llm == "claude":
                return await self._generate_claude(messages, max_tokens, temperature)
            elif llm == "grok":
                return await self._generate_grok(messages, max_tokens, temperature)
            elif llm == "chatgpt":
                return await self._generate_chatgpt(messages, max_tokens, temperature)
            elif llm == "ollama":
                return await self._generate_ollama(messages, max_tokens, temperature)
            else:
                logger.error(f"Unknown LLM: {llm}")
                return None

        except Exception as e:
            logger.error(f"Error generating with {llm}: {e}")
            return None

    async def _generate_claude(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int,
        temperature: float
    ) -> Optional[str]:
        """Generate using Claude (Anthropic)"""
        if not self.anthropic_client:
            logger.warning("Anthropic API key not configured")
            return None

        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages
            )

            if response.content and len(response.content) > 0:
                return response.content[0].text

            return None

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return None

    async def _generate_grok(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int,
        temperature: float
    ) -> Optional[str]:
        """Generate using Grok (xAI) - uses OpenAI-compatible API"""
        if not self.xai_key:
            logger.warning("xAI API key not configured")
            return None

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.xai_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": "grok-beta",
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }

                async with session.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if "choices" in data and len(data["choices"]) > 0:
                            return data["choices"][0]["message"]["content"]

                    logger.error(f"Grok API error: {resp.status}")
                    return None

        except Exception as e:
            logger.error(f"Grok API error: {e}")
            return None

    async def _generate_chatgpt(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int,
        temperature: float
    ) -> Optional[str]:
        """Generate using ChatGPT (OpenAI)"""
        if not self.openai_client:
            logger.warning("OpenAI API key not configured")
            return None

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )

            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content

            return None

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return None

    async def _generate_ollama(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int,
        temperature: float
    ) -> Optional[str]:
        """Generate using local Ollama"""
        try:
            async with aiohttp.ClientSession() as session:
                model = os.getenv("OLLAMA_MODEL", "llama2")

                # Convert messages to Ollama format
                prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                }

                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("response", "")

                    logger.error(f"Ollama API error: {resp.status}")
                    return None

        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            return None


# Example usage
if __name__ == "__main__":
    import asyncio

    async def test():
        router = LLMRouter()

        messages = [
            {"role": "user", "content": "Write a short beach scene description in 50 words."}
        ]

        print("Testing Claude...")
        result = await router.generate(messages, llm="claude", max_tokens=100)
        if result:
            print(f"Claude: {result}\n")

        print("Testing ChatGPT...")
        result = await router.generate(messages, llm="chatgpt", max_tokens=100)
        if result:
            print(f"ChatGPT: {result}\n")

        print("Testing Grok...")
        result = await router.generate(messages, llm="grok", max_tokens=100)
        if result:
            print(f"Grok: {result}\n")

    asyncio.run(test())
