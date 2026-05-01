from sqlalchemy import text

def get_hotspot_files(session):
    query = text("""
        SELECT 
            f.file_path,
            SUM(fc.lines_added + fc.lines_deleted) AS churn
        FROM file_changes fc
        JOIN files f ON fc.file_id = f.id
        GROUP BY f.file_path
        ORDER BY churn DESC
        LIMIT 10;
    """)

    result = session.execute(query)

    return result.fetchall()