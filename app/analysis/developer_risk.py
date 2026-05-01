from sqlalchemy import text

def get_developer_risk(session):
    query = text("""
        SELECT 
            d.name,
            COUNT(c.hash) AS commits,
            SUM(fc.lines_added + fc.lines_deleted) AS churn
        FROM commits c
        JOIN developers d ON c.author_id = d.id
        JOIN file_changes fc ON fc.commit_hash = c.hash
        GROUP BY d.name
        ORDER BY churn DESC
        LIMIT 10;
    """)

    return session.execute(query).fetchall()