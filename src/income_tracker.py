"""
INCOME TRACKER
==============
Track revenue, expenses, and profits from digital product sales.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


class IncomeTracker:
    """Track and analyze income from all sources"""
    
    def __init__(self, data_dir=None):
        self.data_dir = data_dir or Path(__file__).parent / "data"
        self.transactions = []
        self.income_sources = {
            "gumroad": [],
            "etsy": [],
            "creative-market": [],
            "other": []
        }
    
    def add_income(self, source, amount, product_id=None, description=""):
        """Add income transaction"""
        transaction = {
            "id": f"txn_{len(self.transactions) + 1}",
            "date": datetime.now().isoformat(),
            "source": source,
            "amount": amount,
            "product_id": product_id,
            "description": description,
            "type": "income"
        }
        self.transactions.append(transaction)
        self.income_sources[source].append(transaction)
    
    def add_expense(self, amount, category, description=""):
        """Add expense transaction"""
        transaction = {
            "id": f"txn_{len(self.transactions) + 1}",
            "date": datetime.now().isoformat(),
            "source": "expense",
            "amount": -abs(amount),
            "category": category,
            "description": description,
            "type": "expense"
        }
        self.transactions.append(transaction)
    
    def get_daily_summary(self, days=30):
        """Get daily income summary"""
        cutoff = datetime.now() - timedelta(days=days)
        
        daily = defaultdict(lambda: {"income": 0, "expenses": 0, "net": 0})
        
        for txn in self.transactions:
            txn_date = datetime.fromisoformat(txn["date"])
            if txn_date >= cutoff:
                date_key = txn_date.strftime("%Y-%m-%d")
                daily[date_key][txn["type"]] += txn["amount"]
                daily[date_key]["net"] = daily[date_key]["income"] + daily[date_key]["expenses"]
        
        return dict(daily)
    
    def get_monthly_summary(self, months=12):
        """Get monthly income summary"""
        monthly = defaultdict(lambda: {"income": 0, "expenses": 0, "net": 0})
        
        for txn in self.transactions:
            txn_date = datetime.fromisoformat(txn["date"])
            month_key = txn_date.strftime("%Y-%m")
            monthly[month_key][txn["type"]] += txn["amount"]
            monthly[month_key]["net"] = monthly[month_key]["income"] + monthly[month_key]["expenses"]
        
        return dict(monthly)
    
    def get_source_breakdown(self):
        """Get income breakdown by source"""
        breakdown = {}
        
        for source, transactions in self.income_sources.items():
            if source != "other":
                breakdown[source] = {
                    "total": sum(t["amount"] for t in transactions),
                    "count": len(transactions),
                    "avg_per_sale": sum(t["amount"] for t in transactions) / max(len(transactions), 1)
                }
        
        return breakdown
    
    def get_top_products(self, limit=10):
        """Get top performing products"""
        product_income = defaultdict(float)
        
        for txn in self.transactions:
            if txn["type"] == "income" and txn.get("product_id"):
                product_income[txn["product_id"]] += txn["amount"]
        
        sorted_products = sorted(product_income.items(), key=lambda x: x[1], reverse=True)
        return sorted_products[:limit]
    
    def calculate_projection(self):
        """Calculate income projection"""
        daily = self.get_daily_summary(30)
        
        if not daily:
            return {"monthly_projection": 0, "yearly_projection": 0}
        
        # Calculate average daily income
        total_income = sum(d["income"] for d in daily.values())
        days_with_data = len(daily)
        avg_daily = total_income / days_with_data
        
        # Project future income
        monthly = avg_daily * 30
        yearly = avg_daily * 365
        
        return {
            "monthly_projection": round(monthly, 2),
            "yearly_projection": round(yearly, 2),
            "avg_daily_income": round(avg_daily, 2),
            "trend": "growing" if avg_daily > 10 else "stable"
        }
    
    def generate_report(self):
        """Generate comprehensive income report"""
        
        total_income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
        total_expenses = sum(abs(t["amount"]) for t in self.transactions if t["type"] == "expense")
        
        return {
            "generated_at": datetime.now().isoformat(),
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_profit": total_income - total_expenses,
            "source_breakdown": self.get_source_breakdown(),
            "top_products": self.get_top_products(),
            "projection": self.calculate_projection(),
            "recent_transactions": sorted(self.transactions, key=lambda x: x["date"], reverse=True)[:10]
        }
    
    def save_data(self, filepath):
        """Save all data to file"""
        data = {
            "transactions": self.transactions,
            "sources": {k: len(v) for k, v in self.income_sources.items()}
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self, filepath):
        """Load data from file"""
        if os.path.exists(filepath):
            with open(filepath) as f:
                data = json.load(f)
                self.transactions = data.get("transactions", [])


# Demo data generator
def generate_demo_data():
    """Generate demo income data for visualization"""
    tracker = IncomeTracker()
    
    # Add demo transactions
    import random
    
    products = [
        "brush-001", "preset-002", "template-003", 
        "course-004", "software-005", "ebook-006"
    ]
    
    sources = ["gumroad", "etsy"]
    
    # Generate 60 days of transactions
    for day in range(60):
        date = datetime.now() - timedelta(days=60-day)
        
        # Random number of sales per day (0-5)
        num_sales = random.randint(0, 5)
        
        for _ in range(num_sales):
            source = random.choice(sources)
            amount = random.uniform(5, 50)
            product = random.choice(products)
            
            tracker.add_income(
                source=source,
                amount=round(amount, 2),
                product_id=product,
                description=f"Sale of {product}"
            )
    
    # Add some expenses
    expenses = [
        (5.99, "software", "Design tools subscription"),
        (15.00, "marketing", "Ads campaign"),
        (9.99, "hosting", "Server costs"),
    ]
    
    for amount, category, desc in expenses:
        for _ in range(random.randint(3, 8)):
            tracker.add_expense(amount, category, desc)
    
    return tracker


if __name__ == "__main__":
    tracker = generate_demo_data()
    report = tracker.generate_report()
    
    print("=" * 50)
    print("📊 INCOME REPORT")
    print("=" * 50)
    print(f"💰 Total Income: ${report['total_income']:.2f}")
    print(f"📉 Expenses: ${report['total_expenses']:.2f}")
    print(f"✅ Net Profit: ${report['net_profit']:.2f}")
    print(f"📈 Monthly Projection: ${report['projection']['monthly_projection']:.2f}")
    print(f"📈 Yearly Projection: ${report['projection']['yearly_projection']:.2f}")
    print("=" * 50)