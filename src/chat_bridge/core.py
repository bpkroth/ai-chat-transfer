from abc import ABC, abstractmethod
from pathlib import Path

from chat_bridge.models import ExportData


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, input_path: Path) -> ExportData:
        pass


class BaseInjector(ABC):
    @abstractmethod
    def inject(self, data: ExportData, output_path: Path | None, dry_run: bool) -> None:
        pass


class Bridge:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.extractors: dict[str, type[BaseExtractor]] = {}
        self.injectors: dict[str, type[BaseInjector]] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        # These will be populated as we implement them
        from chat_bridge.extractors.claude import ClaudeExtractor
        from chat_bridge.extractors.gemini import GeminiExtractor
        from chat_bridge.injectors.json_injector import JsonInjector
        from chat_bridge.injectors.markdown import MarkdownInjector

        self.extractors["gemini"] = GeminiExtractor
        self.extractors["claude"] = ClaudeExtractor
        self.injectors["markdown"] = MarkdownInjector
        self.injectors["json"] = JsonInjector

    def run(
        self, source: str, input_file: str, target: str, output_file: str | None
    ) -> None:
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
