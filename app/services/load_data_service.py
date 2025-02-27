import time
import requests
from sqlmodel import Session

from services.price_service import PriceService
from services.term_product_service import TermProductService
from services.term_service import TermService
from services.product_service import ProductService

from schemas.term_product_schema import TermProductCreate
from schemas.term_attribute_schema import TermAttributeCreate
from schemas.term_schema import TermCreate
from schemas.price_schema import PriceCreate
from schemas.product_schema import ProductCreate

class LoadDataService:
    URL = 'https://sleakops-interview-tests.s3.us-east-1.amazonaws.com/rds_us_east_1_pricing.json'

    def __init__(self, db: Session):
        self.product_service = ProductService(db)
        self.term_product_service = TermProductService(db)
        self.term_service = TermService(db)
        self.price_service = PriceService(db)

    def fetch_data(self):
        start_time = time.perf_counter()
        response = requests.get(self.URL)
        response.raise_for_status()
        return response.json(), time.perf_counter() - start_time
    
    def process_products(self, products_data):
        start_time = time.perf_counter()
        for sku, product in products_data.items():
            attributes = product.get("attributes", {})
            new_product = ProductCreate(
                sku=sku,
                instance_type=attributes.get("instanceType", ""),
                database_engine=attributes.get("databaseEngine", ""),
                memory=attributes.get("memory", ""),
                vcpu=int(attributes.get("vcpu", 0))
            )
            self.product_service.create_product(new_product)
        return time.perf_counter() - start_time
    
    def process_terms(self, terms_data, term_type):
        start_time = time.perf_counter()
        for sku, term_dict in terms_data.items():
            for term_code, term_details in term_dict.items():
                term_attr = None
                prices = []

                if len(term_details["termAttributes"].keys()) > 0:
                    term_attr = TermAttributeCreate(
                        lease_contract_length=term_details["termAttributes"]["LeaseContractLength"],
                        purchase_option=term_details["termAttributes"]["PurchaseOption"],
                        offering_class=term_details["termAttributes"]["OfferingClass"]
                    )

                for price_code, price_details in term_details.get("priceDimensions", {}).items():
                    currency = next(iter(price_details["pricePerUnit"]))

                    prices.append(PriceCreate(
                        price_code=price_code,
                        term_code=term_code,
                        unit=price_details["unit"],
                        description=price_details["description"],
                        price_per_unit=float(price_details["pricePerUnit"][currency]),
                        currency=currency
                    ))

                self.term_service.get_or_create_term(
                    TermCreate(
                        term_code=term_code,
                        type=term_type,
                        effective_date=term_details["effectiveDate"],
                        term_attribute=term_attr,
                        prices=prices
                    )
                )

                self.term_product_service.add(TermProductCreate(
                    sku=sku,
                    term_code=term_code
                ))

        return time.perf_counter() - start_time

    def load_data(self):
        data, time_fetch = self.fetch_data()
        print(f"Data fetched. Time: {time_fetch:.3f} seconds")
        
        time_process_products = self.process_products(data["products"])
        print(f"Products processed. Time: {time_process_products:.3f} seconds")
        
        time_process_ondeman = self.process_terms(data["terms"].get("OnDemand", {}), "OnDemand")
        print(f"OnDemand terms processed. Time: {time_process_ondeman:.3f} seconds")
        
        time_process_reserver = self.process_terms(data["terms"].get("Reserved", {}), "Reserved")
        print(f"Reserved terms processed. Time: {time_process_reserver:.3f} seconds")

