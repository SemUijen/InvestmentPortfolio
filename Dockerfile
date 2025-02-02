# Fabric Runtime 1.3: 
FROM apache/spark:3.5.0-scala2.12-java11-python3-ubuntu

USER 0
# copy the requirements file
COPY requirements.txt .
# Set the working directory
WORKDIR /src

# Copy the application files
COPY . /src

# Install dependencies
RUN pip install -r requirements.txt

ENV BRONZE_DATA_PATH=/InvestmentPortfolioData/bronze
ENV SILVER_DATA_PATH=/InvestmentPortfolioData/silver
ENV GOLD_DATA_PATH=/InvestmentPortfolioData/gold


CMD ["spark-submit", "--packages", "io.delta:delta-spark_2.12:3.2.0", "src/your_script.py"]