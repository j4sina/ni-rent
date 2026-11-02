from dataclasses import dataclass

@dataclass
class TenantSettlement:
    tenant_id: int                  
    month: int                      
    year: int                       
    apartment_settlement_id: Any    
    rent_share: float               
    utility_share: float            
    total_transfers: float          
    
    @property
    def total_due(self) -> float:
        return self.rent_share + self.utility_share

    @property
    def balance(self) -> float:
                return self.total_transfers - self.total_due
