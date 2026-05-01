from sqlalchemy import text

def get_file_risk_scores(session):
    query = text("""
        SELECT 
            f.file_path,
            COUNT(*) AS change_count,
            SUM(fc.lines_added + fc.lines_deleted) AS churn,

            SUM(
                CASE 
                    WHEN LOWER(c.message) ~ '(fix|bug|error|issue|patch)'
                    THEN 1 ELSE 0
                END
            ) * 1.0 / COUNT(*) AS bug_density,

            SUM(fc.lines_added + fc.lines_deleted) * 
                LN(1 + COUNT(*)) * 
                (1 + (
                    SUM(
                        CASE 
                            WHEN LOWER(c.message) LIKE '%fix%' 
                              OR LOWER(c.message) LIKE '%bug%' 
                              OR LOWER(c.message) LIKE '%error%'
                            THEN 1 ELSE 0
                        END
                    ) * 1.0 / COUNT(*)
                )) AS risk_score

        FROM file_changes fc
        JOIN commits c ON fc.commit_hash = c.hash
        JOIN files f ON fc.file_id = f.id

        WHERE f.file_path LIKE '%.java'
        GROUP BY f.file_path
        ORDER BY risk_score DESC
        LIMIT 10;
    """)

    return session.execute(query).fetchall()

