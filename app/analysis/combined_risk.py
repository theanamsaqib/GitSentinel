from sqlalchemy import text

def get_combined_risk(session):
    query = text("""
        WITH file_risk AS (
            SELECT 
                f.id AS file_id,
                SUM(fc.lines_added + fc.lines_deleted) AS churn,
                COUNT(*) AS change_count,
                SUM(fc.lines_added + fc.lines_deleted) * LOG(1 + COUNT(*)) AS risk_score
            FROM file_changes fc
            JOIN files f ON fc.file_id = f.id
            GROUP BY f.id
        ),
        dev_file_activity AS (
            SELECT
                d.id AS dev_id,
                d.name,
                fc.file_id,
                COUNT(*) AS touches
            FROM file_changes fc
            JOIN commits c ON fc.commit_hash = c.hash
            JOIN developers d ON c.author_id = d.id
            GROUP BY d.id, d.name, fc.file_id
        )
        SELECT
            dfa.name,
            SUM(fr.risk_score * dfa.touches) AS combined_risk
        FROM dev_file_activity dfa
        JOIN file_risk fr ON fr.file_id = dfa.file_id
        GROUP BY dfa.name
        ORDER BY combined_risk DESC
        LIMIT 10;
    """)

    return session.execute(query).fetchall()