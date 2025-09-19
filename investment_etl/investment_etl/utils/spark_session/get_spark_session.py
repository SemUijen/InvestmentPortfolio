from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


def get_spark_session() -> SparkSession:
    builder = (
        SparkSession.builder.appName("MyApp")
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension",
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )

    return configure_spark_with_delta_pip(builder).getOrCreate()
