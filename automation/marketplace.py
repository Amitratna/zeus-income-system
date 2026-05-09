"""
MARKETPLACE AUTOMATION
======================
Automate listing products on Etsy and Gumroad.
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path


class MarketplaceAutomation:
    """Automate listing to Etsy and Gumroad"""
    
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.listings = []
        self.sales = []
    
    def _load_config(self, config_path):
        """Load API credentials"""
        if config_path and os.path.exists(config_path):
            with open(config_path) as f:
                return json.load(f)
        return {
            "etsy": {
                "api_key": os.getenv("ETSY_API_KEY", "demo_key"),
                "shop_id": os.getenv("ETSY_SHOP_ID", "demo_shop")
            },
            "gumroad": {
                "access_token": os.getenv("GUMROAD_TOKEN", "demo_token")
            }
        }
    
    # ==================== GUMROAD ====================
    
    def list_on_gumroad(self, product):
        """List product on Gumroad"""
        print(f"📦 Listing on Gumroad: {product['name']}")
        
        # Simulate Gumroad API call
        # In production, use: POST https://api.gumroad.com/v2/products
        
        listing = {
            "id": f"gumroad_{product['id']}",
            "product_id": product['id'],
            "name": product['name'],
            "description": product['description'],
            "price": product['price'],
            "tags": product.get('tags', []),
            "listed_at": datetime.now().isoformat(),
            "status": "published",
            "url": f"https://gumroad.com/l/{product['id']}",
            "sales_count": 0,
            "revenue": 0.0
        }
        
        self.listings.append(listing)
        return listing
    
    def get_gumroad_sales(self):
        """Fetch sales from Gumroad"""
        # Simulate API call
        return {
            "success": True,
            "sales": [],
            "total_revenue": 0.0
        }
    
    # ==================== ETSY ====================
    
    def list_on_etsy(self, product):
        """List product on Etsy"""
        print(f"🛍️ Listing on Etsy: {product['name']}")
        
        # Simulate Etsy API call
        # In production, use: POST /application/shops/{shop_id}/listings
        
        listing = {
            "id": f"etsy_{product['id']}",
            "product_id": product['id'],
            "title": product['name'],
            "description": product['description'],
            "price": product['price'],
            "tags": product.get('tags', []),
            "listed_at": datetime.now().isoformat(),
            "status": "active",
            "url": f"https://etsy.com/listing/{product['id']}",
            "views": 0,
            "favorites": 0,
            "sales_count": 0
        }
        
        self.listings.append(listing)
        return listing
    
    def get_etsy_sales(self):
        """Fetch sales from Etsy"""
        # Simulate API call
        return {
            "success": True,
            "orders": [],
            "total_revenue": 0.0
        }
    
    # ==================== BATCH OPERATIONS ====================
    
    def list_all(self, products):
        """List all products to their assigned platforms"""
        results = []
        
        for product in products:
            platforms = product.get('platforms', ['gumroad'])
            
            for platform in platforms:
                if platform == 'gumroad':
                    result = self.list_on_gumroad(product)
                elif platform == 'etsy':
                    result = self.list_on_etsy(product)
                else:
                    result = {"platform": platform, "status": "skipped"}
                
                results.append(result)
            
            # Rate limiting
            time.sleep(0.5)
        
        return results
    
    # ==================== ANALYTICS ====================
    
    def get_analytics(self):
        """Get comprehensive analytics"""
        
        gumroad_sales = [l for l in self.listings if l.get('id', '').startswith('gumroad_')]
        etsy_sales = [l for l in self.listings if l.get('id', '').startswith('etsy_')]
        
        return {
            "total_products": len(self.listings),
            "gumroad_listings": len(gumroad_sales),
            "etsy_listings": len(etsy_sales),
            "total_revenue": sum(l.get('price', 0) for l in self.listings),
            "avg_price": sum(l.get('price', 0) for l in self.listings) / max(len(self.listings), 1),
            "listings": self.listings
        }
    
    def save_analytics(self, filepath):
        """Save analytics to file"""
        analytics = self.get_analytics()
        
        with open(filepath, 'w') as f:
            json.dump(analytics, f, indent=2)
        
        return analytics


# Run automation demo
if __name__ == "__main__":
    # Load generated products
    products_file = Path(__file__).parent.parent / "data" / "generated_products.json"
    
    if products_file.exists():
        with open(products_file) as f:
            products = json.load(f)
        
        automation = MarketplaceAutomation()
        results = automation.list_all(products[:5])
        
        print(f"✅ Listed {len(results)} products")
        
        # Save analytics
        data_dir = Path(__file__).parent / "data"
        analytics = automation.save_analytics(data_dir / "marketplace_analytics.json")
        print(f"📊 Analytics saved")
    else:
        print("⚠️ No products found. Run product_generator.py first.")