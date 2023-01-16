from typing import Dict
from app._models import HeimdallModel


# =========================================================
# CLASS ENTITY ADAPTER
# =========================================================
class EntityAdapter(object):

    # -----------------------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------------------
    def __init__(self, destination_model: HeimdallModel, raw_data: Dict):
        self.result = self.extract_entity(
            destination_model=destination_model, raw_data=raw_data
        )

    # -----------------------------------------------------
    # EXTRACT ENTITY
    # -----------------------------------------------------
    @staticmethod
    def extract_entity(destination_model: HeimdallModel, raw_data: dict):
        result = {}
        for key in destination_model.model_fields:
            if key in raw_data.keys():
                result[key] = raw_data[key]
        return result

    # -----------------------------------------------------
    # PROPERTY TRANSFORMED
    # -----------------------------------------------------
    @property
    def transformed(self):
        return self.result
