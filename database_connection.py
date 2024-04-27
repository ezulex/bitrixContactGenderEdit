import psycopg2
import app_logger
import os
from dotenv import load_dotenv

logger = app_logger.get_logger(__name__)
load_dotenv()


def check_name(contact_name):
    """
        This function check name in database
        contact_name: string, name for checking in database
    """
    try:
        connection = psycopg2.connect(
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=os.environ.get("DB_DATABASE")
        )

        cursor = connection.cursor()
        logger.info("Connection to the database is open")

        result = -1

        select_query = '''
            SELECT EXISTS (
                SELECT * FROM names_man WHERE name = %s
            )
        '''
        cursor.execute(select_query, (contact_name,))
        exists_male = cursor.fetchone()[0]
        if exists_male:
            result = 1
        else:
            select_query = '''
                        SELECT EXISTS (
                            SELECT * FROM names_woman WHERE name = %s
                        )
                    '''
            cursor.execute(select_query, (contact_name,))
            exists_female = cursor.fetchone()[0]
            if exists_female:
                result = 0
        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error connection to the database. {error}")
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info("Connection to the database is closed")
