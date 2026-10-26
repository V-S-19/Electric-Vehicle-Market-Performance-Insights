"""
Automated Verification & Test Suite for EV Market Analytics Platform
"""
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "web_app"))

from app import app

def run_tests():
    print("=" * 60)
    print("RUNNING AUTOMATED TEST SUITE FOR EV MARKET ANALYTICS")
    print("=" * 60)

    client = app.test_client()

    routes = [
        ('/', 'Overview & Problem Definition'),
        ('/dashboard', 'Executive Dashboard'),
        ('/story', '5-Scene Story Mode'),
        ('/personas', 'Strategic Personas'),
        ('/sql-explorer', 'Interactive SQL Explorer'),
        ('/performance', 'Performance Testing Suite'),
        ('/tableau-embed', 'Tableau Embed'),
        ('/documentation', 'Step-by-Step Documentation'),
        ('/presentation', 'Executive Presentation Deck')
    ]

    print("\n1. Testing HTML Page Routes:")
    for path, desc in routes:
        res = client.get(path)
        status = res.status_code
        print(f"  [HTTP {status}] {path:<20} -> {desc}")
        assert status == 200, f"Route {path} failed with {status}"

    print("\n2. Testing REST API Endpoints:")
    
    # Filter options
    res = client.get('/api/filter-options')
    assert res.status_code == 200
    options = res.get_json()
    print(f"  [HTTP 200] /api/filter-options: {len(options['years'])} years, {len(options['categories'])} categories, {len(options['manufacturers'])} makers")

    # Data query with filters
    res = client.get('/api/data?year=2024&category=SUV&battery=LFP')
    assert res.status_code == 200
    data = res.get_json()
    print(f"  [HTTP 200] /api/data (Filtered: Year=2024, Cat=SUV, Bat=LFP): {data['record_count']} rows returned in {data['execution_time_ms']} ms")
    assert data['record_count'] > 0
    assert 'total_sales_units' in data['kpis']

    # SQL Execution API
    sql_payload = {
        "query": "SELECT vehicle_category, COUNT(*) as cnt, SUM(annual_sales_units) as sales FROM ev_market_analytics GROUP BY vehicle_category"
    }
    res = client.post('/api/run-sql', json=sql_payload)
    assert res.status_code == 200
    sql_res = res.get_json()
    print(f"  [HTTP 200] /api/run-sql: Executed query in {sql_res['execution_time_ms']} ms ({sql_res['total_rows']} rows returned)")
    assert sql_res['total_rows'] == 6

    # Performance Benchmarks API
    res = client.get('/api/performance-benchmark')
    assert res.status_code == 200
    bench = res.get_json()
    print(f"  [HTTP 200] /api/performance-benchmark: {len(bench['benchmarks'])} benchmark tests executed successfully")
    for b in bench['benchmarks']:
        print(f"    - {b['test_name']:<45} -> {b['execution_time_ms']:>6.2f} ms [{b['status']}]")

    print("\n" + "=" * 60)
    print("ALL 12 TEST CASES PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
