from typing import Optional
from dataclasses import dataclass

@dataclass
class BaseResponse:
    message: Optional[str] = None
    status_code: Optional[int] = None

    def get_json_response(self):
        return {
            'message': self.message,
        }

@dataclass
class BooleanTypeResponse(BaseResponse):
    is_successful: bool = True

