from sqlalchemy import text

def get_file_bug_metrics(session):
    query = text("""
        SELECT 
            f.file_path,
            COUNT(*) AS total_changes,
            SUM(
                CASE 
                    WHEN LOWER(c.message) LIKE '%fix%' 
                      OR LOWER(c.message) LIKE '%bug%' 
                      OR LOWER(c.message) LIKE '%error%'
                    THEN 1 ELSE 0
                END
            ) AS bug_changes,
            SUM(
                CASE 
                    WHEN LOWER(c.message) LIKE '%fix%' 
                      OR LOWER(c.message) LIKE '%bug%' 
                      OR LOWER(c.message) LIKE '%error%'
                    THEN 1 ELSE 0
                END
            ) * 1.0 / COUNT(*) AS bug_density
        FROM file_changes fc
        JOIN commits c ON fc.commit_hash = c.hash
        JOIN files f ON fc.file_id = f.id
        GROUP BY f.file_path
        ORDER BY bug_density DESC
        LIMIT 20;
    """)

    return session.execute(query).fetchall()