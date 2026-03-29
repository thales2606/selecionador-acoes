from typing import Optional
from pydantic import BaseModel


class StockOutputDTO(BaseModel):
    """DTO de saída para um Stock"""
    name: str
    ticker: str
    situation_emissor: str
    ebit: float
    divida_liquida: float
    quantidade_total_acoes: int
    rank_ev_ebit: Optional[int] = None

    class Config:
        from_attributes = True
