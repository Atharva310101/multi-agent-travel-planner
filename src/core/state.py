from dataclasses import dataclass, field
from typing import Optional, List, Dict

# We will pass this object around. It holds the structured data of our trip.
@dataclass
class TripState:
    destination: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    flight: Optional[Dict] = None
    hotel: Optional[Dict] = None
    activities: List[Dict] = field(default_factory=list)

    def to_dict(self):
        return {
            "destination": self.destination,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "flight": self.flight,
            "hotel": self.hotel,
            "activities": self.activities
        }