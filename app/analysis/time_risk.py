from sqlalchemy import text

def get_risk_over_time(session):
    query = text("""
        SELECT 
            DATE_TRUNC('month', c.commit_date) AS month,
            SUM(fc.lines_added + fc.lines_deleted) AS churn
        FROM commits c
        JOIN file_changes fc ON fc.commit_hash = c.hash
        GROUP BY month
        ORDER BY month;
    """)

    return session.execute(query).fetchall()