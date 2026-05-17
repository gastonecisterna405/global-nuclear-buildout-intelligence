from __future__ import annotations
from pathlib import Path

def main() -> None:
    try:
        from pyspark.sql import SparkSession
        import pyspark.sql.functions as F
    except Exception as exc:
        print(f"PySpark is not installed. Install pyspark to run scalable ETL. Reason: {exc}")
        return
    root = Path(__file__).resolve().parents[1]
    spark = SparkSession.builder.appName("global-nuclear-buildout-intelligence").getOrCreate()
    reactors = spark.read.option("header", True).option("inferSchema", True).csv(str(root / "data/processed/reactors_master.csv"))
    out = reactors.groupBy("country","technology_family","status_group").agg(F.sum("capacity_mwe").alias("capacity_mwe"), F.count("*").alias("reactor_count"))
    target = root / "data/analytics/spark_capacity_by_country_technology"
    out.write.mode("overwrite").parquet(str(target))
    print(f"Wrote {target}")
    spark.stop()

if __name__ == "__main__":
    main()
