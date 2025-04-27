from __future__ import annotations
import os
from dataclasses import dataclass, field, fields
from typing import Annotated, Optional
from langchain_core.runnables import RunnableConfig, ensure_config

@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default=f"openai/{os.getenv('OPENAI_MODEL')}",
        metadata={
            "description": "The model to use for the agent."
        },
    )

    recursion_limit: int = field(
        default=25,
        metadata={
            "description": "The recursion limit for the agent."
        },
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> Configuration:
        """Load configuration with defaults for the given invocation."""
        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        _fields = {f.name for f in fields(cls) if f.init}

        # Extract values from the configurable section
        kwargs = {k: v for k, v in configurable.items() if k in _fields}

        # Also allow top-level config keys (like recursion_limit) to override defaults
        for key in _fields:
            if key not in kwargs and key in config:
                kwargs[key] = config[key]

        instance = cls(**kwargs)

        # Copy the model and user_id attributes into the metadata attribute
        metadata = config.get("metadata", {})
        metadata["model"] = instance.model
        config["metadata"] = metadata

        return instance
