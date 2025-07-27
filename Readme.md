# Avrioc Case Study: Real-Time Clickstream Analytics Pipeline

A comprehensive real-time data analytics pipeline that processes clickstream data using Kafka for streaming and ClickHouse for analytics with specialized fact tables and automated monitoring.

## 🏗️ Architecture Overview

This project implements a complete real-time analytics pipeline with the following components:

```
Data Generator → Kafka Producer → Kafka Topic → Specialized Consumers → ClickHouse Fact Tables → Slack Alerts
```

### Key Components

- **Data Generator**: Simulates realistic clickstream data with A/B testing experiments, user sessions, and device tracking
- **Kafka Streaming**: Handles real-time data ingestion and processing with multiple consumer groups
- **ClickHouse Data Warehouse**: High-performance analytics database with specialized fact tables:
  - `fct_user`: User-level interaction analytics
  - `fct_item`: Item-level performance metrics  
  - `fct_experiment`: A/B testing and experiment analytics
- **Slack Monitoring**: Automated alerts for anomalous item sales patterns
- **Connection Testing**: Simple test scripts to verify database connectivity

## 📋 Features

- ✅ Real-time clickstream data generation with rich metadata
- ✅ High-throughput Kafka streaming pipeline with multiple consumer groups
- ✅ Specialized ClickHouse fact tables for different analytics use cases
- ✅ A/B testing and experiment tracking capabilities
- ✅ User behavior and item performance analytics
- ✅ Automated Slack alerts for sales anomalies
- ✅ Configurable batch processing and data aggregation
- ✅ Docker containerization for Kafka infrastructure

## 🛠️ Tech Stack

- **Streaming**: Apache Kafka (Confluent Platform)
- **Database & Analytics**: ClickHouse with specialized fact tables
- **Monitoring & Alerts**: Slack SDK for automated notifications
- **Language**: Python 3.x
- **Containerization**: Docker Compose
- **Data Processing**: Pandas, PyArrow, NumPy

## 🗄️ Database Comparison

The following table compares different database options for real-time analytics:

| Database | Type | Speed | Pricing (for ~13M records/day) | Complexity | Popularity (GitHub stats) |
|----------|------|-------|-------------------------------|------------|---------------------------|
| Druid | Columnar | Sub-second analytics and ingestion | Self-hosted: ~$200/mo infrastructure<br/>Managed: ~$400-800/mo | Moderate-to-high; requires expertise | 13,000+ stars, 67 contributors, ~800 issues |
| Pinot | Columnar | Sub-second response, high concurrency | Self-hosted: ~$150/mo infrastructure<br/>Managed: ~$300-600/mo | Moderate; requires indexing understanding | 5,500+ stars, 100+ contributors, ~600 issues |
| **ClickHouse** | **Columnar** | **Very fast; billions of rows/sec** | **Self-hosted: ~$50-100/mo**<br/>**ClickHouse Cloud: ~$100-250/mo** | **Medium; complex at large scale** | **42,000+ stars, 850+ contributors, ~1,200 issues** |
| Cassandra | Wide Column Store | High write throughput, low latency | Self-hosted: ~$100-200/mo<br/>Managed (DataStax): ~$300-500/mo | High; complex modeling and ops | 8,200+ stars, 350+ contributors, ~350 issues |
| MongoDB | Document DB | Fast for simple queries; slower for analytics | Atlas: ~$200-400/mo<br/>Self-hosted: ~$80-150/mo | Low for basics, moderate for analytics | 24,000+ stars, 600+ contributors, ~1,500 issues |

**ClickHouse was selected for this project** due to its exceptional performance for analytical workloads, strong community support, and optimal balance of complexity versus capability for real-time analytics use cases.

## 📦 Installation & Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- ClickHouse server (local or cloud)
- Slack workspace with bot token (for alerts)
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd avrioc_case_study
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Kafka with Docker**
   ```bash
   docker-compose up -d
   ```

4. **Set environment variables**
   ```bash
   export KAFKA_BROKER_URL="localhost:9092"
   export KAFKA_TOPIC="clickstream_topic"
   export KAFKA_CONSUMER_TIMEOUT_MS="10000"
   export KAFKA_FLUSH_INTERVAL="30"
   export KAFKA_BATCH_SIZE="1000"
   export CLICKHOUSE_HOST="localhost"
   export CLICKHOUSE_USER="default"
   export CLICKHOUSE_PASSWORD=""
   export KAFKA_SECURITY_PROTOCOL="PLAINTEXT"
   export SLACK_BOT_TOKEN="your-slack-bot-token"
   ```

## 🚀 Usage

### Running the Data Pipeline

1. **Start the Kafka Producer** (generates and sends data)
   ```bash
   python src/kafka/producer.py --batch_size 1000 --time_interval 1 --data_generation_speed 10000
   ```

2. **Start the Specialized Consumers** (in separate terminals)
   ```bash
   # Raw clickstream data consumer
   python src/kafka/consumer.py
   
   # User analytics consumer
   python src/data_models/fct_user.py
   
   # Item analytics consumer (includes sales monitoring)
   python src/data_models/fct_item.py
   
   # Experiment analytics consumer
   python src/data_models/fct_experiment.py
   ```

3. **Monitor Sales Alerts**
   
   The `fct_item.py` consumer automatically triggers Slack alerts when item sales exceed statistical thresholds.

### Configuration Options

#### Producer Parameters
- `--batch_size`: Number of records per batch (default: 1000)
- `--time_interval`: Time interval between batches in seconds (default: 1)
- `--data_generation_speed`: Speed multiplier for data generation (default: 10000)

#### Data Schema
The generated clickstream data includes:
- **Core Data**: `user_id`, `item_id`, `interaction_type`, `timestamp`
- **Experiment Metadata**: `experiment_name`, `experiment_variation`
- **Session Data**: `session_id`, `device_name`

#### Fact Tables Structure
- **fct_user**: User-level aggregations (total interactions, purchases, views, clicks)
- **fct_item**: Item-level performance metrics with anomaly detection
- **fct_experiment**: A/B testing results and experiment performance

## 📊 Analytics & Monitoring Features

### ClickHouse Analytics
- **Specialized Fact Tables**: Pre-aggregated data for efficient querying
- **Real-time Metrics**: Live dashboards for user behavior and item performance
- **A/B Testing Analytics**: Experiment performance tracking and statistical analysis
- **High-Performance Queries**: Optimized for time-series analytics

### Slack Monitoring
- **Automated Alerts**: Sales anomaly detection using statistical thresholds
- **Real-time Notifications**: Immediate alerts when items exceed 1.5x average sales
- **Customizable Thresholds**: Configurable monitoring parameters

## 🧪 Testing & Verification

### Connection Tests
Run simple connection verification tests:

```bash
# Test database connections
python test/test_clickhouse.py
python test/test_druid.py
python test/test_mongo_db.py

# Test Kafka components
python test/kafka_producer.py
python test/kafka_consumer.py
```

*Note: Test scripts verify basic connectivity and are not comprehensive test suites.*

## 📁 Project Structure

```
avrioc_case_study/
├── docker-compose.yml          # Kafka container setup
├── requirements.txt            # Python dependencies
├── src/
│   ├── data_models/           # Specialized analytics consumers
│   │   ├── fct_experiment.py  # A/B testing analytics
│   │   ├── fct_item.py        # Item performance analytics
│   │   └── fct_user.py        # User behavior analytics
│   ├── kafka/
│   │   ├── data_generator.py  # Rich clickstream data generation
│   │   ├── producer.py        # Kafka producer with auto-topic creation
│   │   └── consumer.py        # Base consumer with ClickHouse integration
│   └── slack_alerts/
│       └── monitor_item_sales.py # Sales anomaly detection & alerts
└── test/
    ├── test_clickhouse.py     # ClickHouse connection test
    ├── test_druid.py          # Druid connection test
    ├── test_mongo_db.py       # MongoDB connection test
    ├── kafka_producer.py      # Kafka producer connection test
    └── kafka_consumer.py      # Kafka consumer connection test
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `KAFKA_BROKER_URL` | Kafka broker connection string | `localhost:9092` |
| `KAFKA_TOPIC` | Kafka topic name | `clickstream_topic` |
| `KAFKA_CONSUMER_TIMEOUT_MS` | Consumer poll timeout | `10000` |
| `KAFKA_FLUSH_INTERVAL` | Data flush interval (seconds) | `30` |
| `KAFKA_BATCH_SIZE` | Consumer batch size | `1000` |
| `CLICKHOUSE_HOST` | ClickHouse server host | `localhost` |
| `CLICKHOUSE_USER` | ClickHouse username | `default` |
| `CLICKHOUSE_PASSWORD` | ClickHouse password | `` |
| `KAFKA_SECURITY_PROTOCOL` | Kafka security protocol | `PLAINTEXT` |
| `SLACK_BOT_TOKEN` | Slack bot token for alerts | Required for monitoring |

## 🐛 Troubleshooting

### Common Issues

1. **Kafka Connection Error**
   - Ensure Docker containers are running: `docker-compose ps`
   - Check Kafka broker URL and port accessibility

2. **ClickHouse Connection Error**
   - Verify ClickHouse server is running and accessible
   - Check connection parameters and credentials
   - Ensure secure connection settings match your ClickHouse setup

3. **No Data in Fact Tables**
   - Ensure Kafka producer is running and generating data
   - Check that appropriate consumers are running for each fact table
   - Verify consumer group names don't conflict

4. **Slack Alerts Not Working**
   - Verify `SLACK_BOT_TOKEN` environment variable is set
   - Ensure bot has permissions to post in the target channel
   - Check that item sales data exists in `fct_item` table

### Logs and Monitoring

- View Kafka logs: `docker-compose logs kafka`
- Monitor topic: `docker exec -it <kafka-container> kafka-topics --list --bootstrap-server localhost:9092`
- Check ClickHouse tables: Query `SHOW TABLES` in ClickHouse client

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Additional Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [ClickHouse Documentation](https://clickhouse.com/docs)
- [ClickHouse SQL Reference](https://clickhouse.com/docs/en/sql-reference)
- [Slack SDK Documentation](https://slack.dev/python-slack-sdk/)

---

**Note**: This is a demonstration project for educational and case study purposes. For production use, additional security, monitoring, and error handling should be implemented.
