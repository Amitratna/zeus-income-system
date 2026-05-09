#!/usr/bin/env python3
"""
ZEUS INCOME SYSTEM - MAIN ORCHESTRATOR
=======================================
Tie together product generation, marketplace listing, and income tracking.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from product_generator import ProductGenerator
from automation.marketplace import MarketplaceAutomation
from src.income_tracker import IncomeTracker


class ZeusIncomeOrchestrator:
    """Main orchestrator for the entire income system"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.generator = ProductGenerator()
        self.automation = MarketplaceAutomation()
        self.tracker = IncomeTracker(self.data_dir)
        
        self.products_file = self.data_dir / "generated_products.json"
        self.analytics_file = self.data_dir / "marketplace_analytics.json"
        
    def run_full_cycle(self, num_products=10):
        """Run complete product creation and listing cycle"""
        print("=" * 60)
        print("⚡ ZEUS INCOME SYSTEM - FULL CYCLE")
        print("=" * 60)
        
        # Phase 1: Generate Products
        print("\n📦 PHASE 1: Product Generation")
        print("-" * 40)
        
        products = self.generator.generate_batch(num_products)
        
        # Save products
        self.generator.save_products(self.products_file)
        
        print(f"✅ Generated {len(products)} products")
        
        # Phase 2: List to Marketplaces
        print("\n🛒 PHASE 2: Marketplace Listing")
        print("-" * 40)
        
        listings = self.automation.list_all(products)
        
        print(f"✅ Listed to {len(listings)} platforms")
        
        # Save analytics
        self.automation.save_analytics(self.analytics_file)
        
        # Phase 3: Track Income
        print("\n💰 PHASE 3: Income Tracking")
        print("-" * 40)
        
        # Simulate some income
        for product in products[:3]:
            self.tracker.add_income(
                source="gumroad",
                amount=product['price'],
                product_id=product['id'],
                description=f"Initial sale of {product['name']}"
            )
        
        # Add some demo expenses
        self.tracker.add_expense(5.99, "software", "Monthly subscription")
        
        # Save tracking data
        self.tracker.save_data(self.data_dir / "income_data.json")
        
        # Phase 4: Generate Report
        print("\n📊 PHASE 4: Analytics Report")
        print("-" * 40)
        
        report = self.tracker.generate_report()
        
        print(f"""
┌─────────────────────────────────────────────────────────┐
│                    INCOME SUMMARY                        │
├─────────────────────────────────────────────────────────┤
│  Total Products Generated: {len(products):<30}│
│  Total Listings: {len(listings):<35}│
│  Total Revenue: ${report['total_income']:<30.2f}│
│  Net Profit: ${report['net_profit']:<32.2f}│
│  Monthly Projection: ${report['projection']['monthly_projection']:<25.2f}│
│  Yearly Projection: ${report['projection']['yearly_projection']:<26.2f}│
└─────────────────────────────────────────────────────────┘
        """)
        
        print("\n✅ Full cycle complete!")
        
        return {
            "products": len(products),
            "listings": len(listings),
            "revenue": report['total_income'],
            "projection": report['projection']
        }
    
    def generate_products_only(self, count=20):
        """Generate products without listing"""
        print(f"🎨 Generating {count} products...")
        
        products = self.generator.generate_batch(count)
        
        self.generator.save_products(self.products_file)
        
        total_value = sum(p['price'] for p in products)
        
        print(f"✅ Generated {count} products")
        print(f"💰 Total potential value: ${total_value:.2f}")
        
        return products
    
    def list_products_only(self):
        """List existing products to marketplaces"""
        if not self.products_file.exists():
            print("⚠️ No products found. Generate products first.")
            return
        
        with open(self.products_file) as f:
            products = json.load(f)
        
        print(f"📤 Listing {len(products)} products...")
        
        listings = self.automation.list_all(products)
        
        self.automation.save_analytics(self.analytics_file)
        
        print(f"✅ Listed to {len(listings)} platforms")
        
        return listings
    
    def show_analytics(self):
        """Show current analytics"""
        print("\n📊 ANALYTICS DASHBOARD")
        print("=" * 50)
        
        if self.analytics_file.exists():
            with open(self.analytics_file) as f:
                analytics = json.load(f)
            
            print(f"""
Total Products: {analytics.get('total_products', 0)}
Gumroad Listings: {analytics.get('gumroad_listings', 0)}
Etsy Listings: {analytics.get('etsy_listings', 0)}
Total Revenue: ${analytics.get('total_revenue', 0):.2f}
Average Price: ${analytics.get('avg_price', 0):.2f}
            """)
        
        report = self.tracker.generate_report()
        
        print(f"""
PROJECTIONS:
Monthly: ${report['projection']['monthly_projection']:.2f}
Yearly: ${report['projection']['yearly_projection']:.2f}
Trend: {report['projection']['trend']}
        """)
        
        return analytics if self.analytics_file.exists() else {}


# CLI Interface
if __name__ == "__main__":
    orchestrator = ZeusIncomeOrchestrator()
    
    if len(sys.argv) < 2:
        print("""
ZEUS INCOME SYSTEM CLI
=====================

Usage:
    python orchestrator.py generate [count]   - Generate products
    python orchestrator.py list                - List products to marketplaces
    python orchestrator.py analytics          - Show analytics
    python orchestrator.py run                 - Full cycle (generate + list)
    python orchestrator.py dashboard           - Start web dashboard
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "generate":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        orchestrator.generate_products_only(count)
    
    elif command == "list":
        orchestrator.list_products_only()
    
    elif command == "analytics":
        orchestrator.show_analytics()
    
    elif command == "run":
        orchestrator.run_full_cycle(10)
    
    elif command == "dashboard":
        print("🚀 Starting dashboard...")
        print("Open http://localhost:5000 in your browser")
        
        # Simple Flask server for dashboard
        from flask import Flask, send_file
        
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            return send_file(Path(__file__).parent / "dashboard" / "index.html")
        
        app.run(host='0.0.0.0', port=5000, debug=True)
    
    else:
        print(f"Unknown command: {command}")