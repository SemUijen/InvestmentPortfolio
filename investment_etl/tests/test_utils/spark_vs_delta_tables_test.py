import re
from investment_etl.utils import DeltaLakeTable, SparkTable
from pyspark.sql.types import StructField, IntegerType, LongType, ByteType, ShortType
import pyarrow as pa
from pyarrow.types import is_date, is_decimal
class DeltaLakeVsSparkTablesTest:
    def _test_class_initialization(self, spark_table: SparkTable, deltalake_table: DeltaLakeTable):
        """Test that both table types initialize correctly with consistent attributes."""
        assert isinstance(spark_table, SparkTable)
        assert isinstance(deltalake_table, DeltaLakeTable)

        # Test common attributes
        assert spark_table.medaillon_layer == deltalake_table.medaillon_layer 
        assert spark_table.table_name == deltalake_table.table_name 
        
        # Test that both implementations have consistent path structure
        assert spark_table.silver_path == deltalake_table.silver_path
        assert spark_table.silver_path.name == deltalake_table.silver_path.name

        assert spark_table.return_primary_keys_columns() == deltalake_table.return_primary_keys_columns()

    def _normalize_deltalake_types(self, field: pa.Field) -> str:
        """Normalize data type strings for comparison using regex patterns."""

        if is_date(field.type):
            return field.name, "date"
        if is_decimal(field.type):
            precision = field.type.precision
            scale = field.type.scale
            return field.name, f"decimal({precision},{scale})"
        return field.name, field.type.__str__()

    def _normalize_pyspark_type(self, field: StructField) -> tuple[str, str]:
        """Normalize PySpark data types for comparison."""
        if isinstance(field.dataType, IntegerType):
            return field.name, "int32"
        elif isinstance(field.dataType, LongType):
            return field.name, "int64"
        elif isinstance(field.dataType, ByteType):
            return field.name, "int8"
        elif isinstance(field.dataType, ShortType):
            return field.name, "int16"
        else:
            return field.name, field.dataType.simpleString()
        
    def _test_equality_of_schemas(self, spark_table: SparkTable, deltalake_table: DeltaLakeTable):
        """Test that both table types have equivalent schemas."""
        spark_schema = spark_table.return_defined_schema()
        deltalake_schema = deltalake_table.return_defined_schema()

        # Convert Spark schema to a comparable format (list of tuples)
        spark_fields = [self._normalize_pyspark_type(field) for field in spark_schema.fields]
        deltalake_fields = [self._normalize_deltalake_types(field) for field in deltalake_schema]

        assert sorted(spark_fields) == sorted(deltalake_fields)
        
    def run_all_tests(self, spark_table: SparkTable, deltalake_table: DeltaLakeTable):
        self._test_class_initialization(spark_table, deltalake_table)
        self._test_equality_of_schemas(spark_table, deltalake_table)
