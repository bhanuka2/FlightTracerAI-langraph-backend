from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_table_info():
    inspector = inspect(engine)
    try:
        table_names = inspector.get_table_names()
        schema_info = {}

        for table_name in table_names:
            columns_info = inspector.get_columns(table_name)

            schema_info[table_name] = []
            for column in columns_info:
                col_details = {
                    "name": column['name'],
                    "type": str(column['type']),
                    "nullable": column['nullable'],
                    "default": column.get('default'),
                    "primary_key": column.get('primary_key', False)
                }
                schema_info[table_name].append(col_details)

        return {
            "database_schema": schema_info,
            "total_tables": len(table_names),
            "table_names": table_names
        }
    except Exception as e:
        return {"error": f"Failed to get database schema: {str(e)}"}


