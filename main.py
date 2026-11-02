from dataclasses import dataclass

from pydantic import BaseModel
from typing import Dict, List, Any

import json


class Parameters(BaseModel):
    apartments_json_path: str = 'data/apartments.json'
    tenants_json_path: str = 'data/tenants.json'
    transfers_json_path: str = 'data/transfers.json'
    bills_json_path: str = 'data/bills.json'


class Room(BaseModel):
    name: str
    area_m2: float


class Apartment(BaseModel):
    key: str
    name: str
    location: str
    area_m2: float
    rooms: Dict[str, Room]

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str,'Apartment']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of apartments"
        return {key: Apartment(**apartment) for key, apartment in data.items()}

    
class Tenant(BaseModel):
    name: str
    apartment: str
    room: str
    rent_pln: float
    deposit_pln: float
    date_agreement_from: str
    date_agreement_to: str

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str,'Tenant']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of tenants"
        return {key: Tenant(**tenant) for key, tenant in data.items()}
    

class Transfer(BaseModel):
    amount_pln: float
    date: str
    settlement_year: int | None
    settlement_month: int | None
    tenant: str

    @staticmethod
    def from_json_file(file_path: str) -> List['Transfer']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of transfers"
        return [Transfer(**transfer) for transfer in data]


class Bill(BaseModel):
    amount_pln: float
    date_due: str
    apartment: str
    settlement_year: int
    settlement_month: int
    type: str

    @staticmethod
    def from_json_file(file_path: str) -> List['Bill']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, list), "Expected a list of bills"
        return [Bill(**bill) for bill in data]


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

class ApartmentSettlement:
    def __init__(self, apartment: str, name: str, rent_pln: float):
        self.apartment = apartment
        self.name = name
        self.rent_pln = rent_pln

    def calculate_annual_rent(self) -> float:
        return self.rent_pln * 12

    def display_settlement_info(self):
        print(f"Apartment: {self.apartment}")
        print(f"Resident Name: {self.name}")
        print(f"Monthly Rent: {self.rent_pln:.2f} PLN")
        print(f"Annual Rent: {self.calculate_annual_rent():.2f} PLN")


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



if __name__ == '__main__':
    parameters = Parameters()
    manager = Manager(parameters)

    for apartment in manager.apartments.values():
        print(f"Klucz: {apartment.key} | Mieszkanie: {apartment.name} | Miejsce: {apartment.location} | Powierzchnia: {apartment.area_m2}")
        for room in apartment.rooms.values():
            print(f"  Pokój: {room.name} | Powierzchnia: {room.area_m2}")
        
        for bill in manager.bills:
            if bill.apartment == apartment.key:
                print(f"  Kwota: {bill.amount_pln} | Termin: {bill.date_due} | Rok: {bill.settlement_year} | Miesiąc: {bill.settlement_month} | Typ: {bill.type}")

    for tenant in manager.tenants.values():
        print(f"Najemca: {tenant.name} | Mieszkanie: {tenant.apartment} | Pokój: {tenant.room} | Czynsz: {tenant.rent_pln} | Kaucja: {tenant.deposit_pln} | Umowa od: {tenant.date_agreement_from} | Umowa do: {tenant.date_agreement_to}")
        for transfer in manager.transfers:
            if transfer.tenant == tenant.name:
                print(f"  Kwota: {transfer.amount_pln} | Data: {transfer.date} | Rok: {transfer.settlement_year} | Miesiąc: {transfer.settlement_month}")
