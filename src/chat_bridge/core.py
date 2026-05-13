"""Core logic and base classes for chat history migration."""

import importlib
from abc import ABC, abstractmethod
from pathlib import Path

from chat_bridge.models import ExportData


class BaseExtractor(ABC):
    """Base class for all chat history extractors."""

    @abstractmethod
    def extract(self, input_path: Path) -> ExportData:
        """Extract chat history from the given path."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class BaseInjector(ABC):
    """Base class for all chat history injectors."""

    @abstractmethod
    def inject(self, data: ExportData, output_path: Path | None, dry_run: bool) -> None:
        """Inject chat history into the target format/agent."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Bridge:
    """Main orchestrator for migrating chat history."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.extractors: dict[str, type[BaseExtractor]] = {}
        self.injectors: dict[str, type[BaseInjector]] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register the built-in extractors and injectors."""
        # Use dynamic loading to satisfy pylint and avoid circular imports
        plugins = {
            "extractors": {
                "gemini": "chat_bridge.extractors.gemini.GeminiExtractor",
                "claude": "chat_bridge.extractors.claude.ClaudeExtractor",
            },
            "injectors": {
                "markdown": "chat_bridge.injectors.markdown.MarkdownInjector",
                "json": "chat_bridge.injectors.json_injector.JsonInjector",
            },
        }

        for name, path in plugins["extractors"].items():
            module_path, class_name = path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            self.extractors[name] = getattr(module, class_name)

        for name, path in plugins["injectors"].items():
            module_path, class_name = path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            self.injectors[name] = getattr(module, class_name)

    def get_supported_sources(self) -> list[str]:
        """Return a list of supported source agents."""
        return sorted(self.extractors.keys())

    def get_supported_targets(self) -> list[str]:
        """Return a list of supported target formats."""
        return sorted(self.injectors.keys())

    def run(
        self, source: str, input_file: str, target: str, output_file: str | None
    ) -> None:
        """Execute the migration from source to target."""
        if source not in self.extractors:
            raise ValueError(f"Unsupported source: {source}")
        if target not in self.injectors:
            raise ValueError(f"Unsupported target: {target}")

        extractor = self.extractors[source]()
        injector = self.injectors[target]()

        input_path = Path(input_file)
        output_path = Path(output_file) if output_file else None

        data = extractor.extract(input_path)
        injector.inject(data, output_path, self.dry_run)
