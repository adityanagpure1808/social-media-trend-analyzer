from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional

class Report(BaseModel):
    id: str
    platform: str
    status: str
    progress: int = 0

    title: Optional[str]
    summary: Optional[str]

    trending_topics: Optional[List[Dict]]
    sentiment_analysis: Optional[Dict]

    error_message: Optional[str]
    created_at: datetime
