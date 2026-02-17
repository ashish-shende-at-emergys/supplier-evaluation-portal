from datetime import date
from models import Supplier, Capability, Region, CostModel, PerformanceRating, ContactInfo

def main():
    # Create a supplier instance
    supplier = Supplier(
        name="Acme Corp",
        contact_info=ContactInfo(
            email="contact@acmecorp.com",
            phone="+1-555-0100",
            address="123 Industrial Way, Tech City"
        ),
        capabilities=[
            Capability(
                category="Manufacturing",
                services=["CNC Machining", "3D Printing"],
                certifications=["ISO 9001"]
            )
        ],
        regions=[
            Region(country="USA", state_province="CA", service_radius_km=500)
        ],
        pricing=[
            CostModel(item_name="Widget A", unit_cost=10.50, currency="USD", bulk_discount_available=True)
        ],
        ratings=[
            PerformanceRating(
                period_start=date(2023, 1, 1),
                period_end=date(2023, 6, 30),
                quality_score=9.5,
                timeliness_score=8.0,
                communication_score=9.0,
                reviewer_comments="Excellent quality, slightly delayed shipment."
            )
        ]
    )

    # Calculate overall score
    print(f"Initial Overall Score: {supplier.overall_score}")
    supplier.calculate_overall_score()
    print(f"Calculated Overall Score: {supplier.overall_score}")

    # Assess Risk
    risk = supplier.assess_risk()
    print(f"Calculated Risk Level: {risk}")

    # Export to JSON
    print("\nSupplier JSON:")
    print(supplier.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
