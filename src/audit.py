import logging

logger = logging.getLogger(__name__)

def insert_audit_record(
        db_connection,
        records_extracted,
        records_loaded,
        status
):
    cursor = db_connection.cursor()
    query = """
    INSERT INTO pipeline_audit (records_extracted, records_loaded, status)
    values (%s, %s, %s)"""

    cursor.execute(query,(
        records_extracted, records_loaded, status))
    

    db_connection.commit()
    cursor.close()
    logger.info(f"Inserted audit record: extracted={records_extracted}, loaded={records_loaded}, status={status}")
