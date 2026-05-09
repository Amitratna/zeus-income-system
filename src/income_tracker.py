     1|"""
     2|INCOME TRACKER
     3|==============
     4|Track revenue, expenses, and profits from digital product sales.
     5|"""
     6|
     7|import json
     8|from datetime import datetime, timedelta
     9|from pathlib import Path
    10|from collections import defaultdict
import os
    11|
    12|
    13|class IncomeTracker:
    14|    """Track and analyze income from all sources"""
    15|    
    16|    def __init__(self, data_dir=None):
    17|        self.data_dir = data_dir or Path(__file__).parent / "data"
    18|        self.transactions = []
    19|        self.income_sources = {
    20|            "gumroad": [],
    21|            "etsy": [],
    22|            "creative-market": [],
    23|            "other": []
    24|        }
    25|    
    26|    def add_income(self, source, amount, product_id=None, description=""):
    27|        """Add income transaction"""
    28|        transaction = {
    29|            "id": f"txn_{len(self.transactions) + 1}",
    30|            "date": datetime.now().isoformat(),
    31|            "source": source,
    32|            "amount": amount,
    33|            "product_id": product_id,
    34|            "description": description,
    35|            "type": "income"
    36|        }
    37|        self.transactions.append(transaction)
    38|        self.income_sources[source].append(transaction)
    39|    
    40|    def add_expense(self, amount, category, description=""):
    41|        """Add expense transaction"""
    42|        transaction = {
    43|            "id": f"txn_{len(self.transactions) + 1}",
    44|            "date": datetime.now().isoformat(),
    45|            "source": "expense",
    46|            "amount": -abs(amount),
    47|            "category": category,
    48|            "description": description,
    49|            "type": "expense"
    50|        }
    51|        self.transactions.append(transaction)
    52|    
    53|    def get_daily_summary(self, days=30):
    54|        """Get daily income summary"""
    55|        cutoff = datetime.now() - timedelta(days=days)
    56|        
    57|        daily = defaultdict(lambda: {"income": 0, "expenses": 0, "net": 0})
    58|        
    59|        for txn in self.transactions:
    60|            txn_date = datetime.fromisoformat(txn["date"])
    61|            if txn_date >= cutoff:
    62|                date_key = txn_date.strftime("%Y-%m-%d")
    63|                daily[date_key][txn["type"]] += txn["amount"]
    64|                daily[date_key]["net"] = daily[date_key]["income"] + daily[date_key]["expenses"]
    65|        
    66|        return dict(daily)
    67|    
    68|    def get_monthly_summary(self, months=12):
    69|        """Get monthly income summary"""
    70|        monthly = defaultdict(lambda: {"income": 0, "expenses": 0, "net": 0})
    71|        
    72|        for txn in self.transactions:
    73|            txn_date = datetime.fromisoformat(txn["date"])
    74|            month_key = txn_date.strftime("%Y-%m")
    75|            monthly[month_key][txn["type"]] += txn["amount"]
    76|            monthly[month_key]["net"] = monthly[month_key]["income"] + monthly[month_key]["expenses"]
    77|        
    78|        return dict(monthly)
    79|    
    80|    def get_source_breakdown(self):
    81|        """Get income breakdown by source"""
    82|        breakdown = {}
    83|        
    84|        for source, transactions in self.income_sources.items():
    85|            if source != "other":
    86|                breakdown[source] = {
    87|                    "total": sum(t["amount"] for t in transactions),
    88|                    "count": len(transactions),
    89|                    "avg_per_sale": sum(t["amount"] for t in transactions) / max(len(transactions), 1)
    90|                }
    91|        
    92|        return breakdown
    93|    
    94|    def get_top_products(self, limit=10):
    95|        """Get top performing products"""
    96|        product_income = defaultdict(float)
    97|        
    98|        for txn in self.transactions:
    99|            if txn["type"] == "income" and txn.get("product_id"):
   100|                product_income[txn["product_id"]] += txn["amount"]
   101|        
   102|        sorted_products = sorted(product_income.items(), key=lambda x: x[1], reverse=True)
   103|        return sorted_products[:limit]
   104|    
   105|    def calculate_projection(self):
   106|        """Calculate income projection"""
   107|        daily = self.get_daily_summary(30)
   108|        
   109|        if not daily:
   110|            return {"monthly_projection": 0, "yearly_projection": 0}
   111|        
   112|        # Calculate average daily income
   113|        total_income = sum(d["income"] for d in daily.values())
   114|        days_with_data = len(daily)
   115|        avg_daily = total_income / days_with_data
   116|        
   117|        # Project future income
   118|        monthly = avg_daily * 30
   119|        yearly = avg_daily * 365
   120|        
   121|        return {
   122|            "monthly_projection": round(monthly, 2),
   123|            "yearly_projection": round(yearly, 2),
   124|            "avg_daily_income": round(avg_daily, 2),
   125|            "trend": "growing" if avg_daily > 10 else "stable"
   126|        }
   127|    
   128|    def generate_report(self):
   129|        """Generate comprehensive income report"""
   130|        
   131|        total_income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
   132|        total_expenses = sum(abs(t["amount"]) for t in self.transactions if t["type"] == "expense")
   133|        
   134|        return {
   135|            "generated_at": datetime.now().isoformat(),
   136|            "total_income": total_income,
   137|            "total_expenses": total_expenses,
   138|            "net_profit": total_income - total_expenses,
   139|            "source_breakdown": self.get_source_breakdown(),
   140|            "top_products": self.get_top_products(),
   141|            "projection": self.calculate_projection(),
   142|            "recent_transactions": sorted(self.transactions, key=lambda x: x["date"], reverse=True)[:10]
   143|        }
   144|    
   145|    def save_data(self, filepath):
   146|        """Save all data to file"""
   147|        data = {
   148|            "transactions": self.transactions,
   149|            "sources": {k: len(v) for k, v in self.income_sources.items()}
   150|        }
   151|        
   152|        with open(filepath, 'w') as f:
   153|            json.dump(data, f, indent=2)
   154|    
   155|    def load_data(self, filepath):
   156|        """Load data from file"""
   157|        if os.path.exists(filepath):
   158|            with open(filepath) as f:
   159|                data = json.load(f)
   160|                self.transactions = data.get("transactions", [])
   161|
   162|
   163|# Demo data generator
   164|def generate_demo_data():
   165|    """Generate demo income data for visualization"""
   166|    tracker = IncomeTracker()
   167|    
   168|    # Add demo transactions
   169|    import random
   170|    
   171|    products = [
   172|        "brush-001", "preset-002", "template-003", 
   173|        "course-004", "software-005", "ebook-006"
   174|    ]
   175|    
   176|    sources = ["gumroad", "etsy"]
   177|    
   178|    # Generate 60 days of transactions
   179|    for day in range(60):
   180|        date = datetime.now() - timedelta(days=60-day)
   181|        
   182|        # Random number of sales per day (0-5)
   183|        num_sales = random.randint(0, 5)
   184|        
   185|        for _ in range(num_sales):
   186|            source = random.choice(sources)
   187|            amount = random.uniform(5, 50)
   188|            product = random.choice(products)
   189|            
   190|            tracker.add_income(
   191|                source=source,
   192|                amount=round(amount, 2),
   193|                product_id=product,
   194|                description=f"Sale of {product}"
   195|            )
   196|    
   197|    # Add some expenses
   198|    expenses = [
   199|        (5.99, "software", "Design tools subscription"),
   200|        (15.00, "marketing", "Ads campaign"),
   201|        (9.99, "hosting", "Server costs"),
   202|    ]
   203|    
   204|    for amount, category, desc in expenses:
   205|        for _ in range(random.randint(3, 8)):
   206|            tracker.add_expense(amount, category, desc)
   207|    
   208|    return tracker
   209|
   210|
   211|if __name__ == "__main__":
   212|    tracker = generate_demo_data()
   213|    report = tracker.generate_report()
   214|    
   215|    print("=" * 50)
   216|    print("📊 INCOME REPORT")
   217|    print("=" * 50)
   218|    print(f"💰 Total Income: ${report['total_income']:.2f}")
   219|    print(f"📉 Expenses: ${report['total_expenses']:.2f}")
   220|    print(f"✅ Net Profit: ${report['net_profit']:.2f}")
   221|    print(f"📈 Monthly Projection: ${report['projection']['monthly_projection']:.2f}")
   222|    print(f"📈 Yearly Projection: ${report['projection']['yearly_projection']:.2f}")
   223|    print("=" * 50)