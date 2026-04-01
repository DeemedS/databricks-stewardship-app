import importlib
from pathlib import Path

from pydantic import BaseModel


def discover_models():
    model_map = {}
    model_dir = Path(__file__).resolve().parents[1] / "models"
    for model_file in model_dir.glob("*.py"):
        module_name = model_file.stem
        module = importlib.import_module(f"models.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, BaseModel) and attr is not BaseModel:
                model_fields = getattr(attr, "model_fields", None)
                if model_fields is not None:
                    field_names = list(model_fields.keys())
                else:
                    field_names = list(attr.__fields__.keys())
                model_map[module_name] = field_names
                break
    return model_map


MODEL_DEFS = discover_models()

