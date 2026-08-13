"""Register vendored OpenAPI client as package name ``adapters_api``."""
import importlib.util
import sys
from pathlib import Path


def _ensure_adapters_api() -> None:
    if "adapters_api" in sys.modules:
        return
    try:
        import adapters_api  # noqa: F401
        return
    except ImportError:
        pass

    adapters_dir = Path(__file__).resolve().parent / "adapters_api"
    init_file = adapters_dir / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        "adapters_api",
        init_file,
        submodule_search_locations=[str(adapters_dir)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load adapters_api from {adapters_dir}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["adapters_api"] = module
    spec.loader.exec_module(module)


_ensure_adapters_api()
