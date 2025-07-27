# Avrioc Case Study: Real-Time Clickstream Analytics Pipeline

A comprehensive real-time data analytics pipeline that processes clickstream data using Kafka for streaming and ClickHouse for storage and analytics.

## 🏗️ Architecture Overview

This project implements a complete real-time analytics pipeline with the following components:

```
Data Generator → Kafka Producer → Kafka Topic → Kafka Consumer → ClickHouse (with built-in dashboard)
```

### Key Components

- **Data Generator**: Simulates realistic clickstream data (user interactions, clicks, views, purchases)
- **Kafka Streaming**: Handles real-time data ingestion and processing
- **ClickHouse Database**: High-performance analytics database for data storage with built-in dashboard capabilities
- **Comprehensive Testing**: Test suites for all major components

## 📋 Features

- ✅ Real-time clickstream data generation
- ✅ High-throughput Kafka streaming pipeline
- ✅ Scalable ClickHouse data warehouse
- ✅ Interactive analytics dashboard
- ✅ Configurable batch processing
- ✅ Docker containerization
- ✅ Comprehensive testing suite

## 🛠️ Tech Stack

- **Streaming**: Apache Kafka (Confluent Platform)
- **Database**: ClickHouse
- **Visualization**: Streamlit + Plotly
- **Language**: Python 3.x
- **Containerization**: Docker Compose
- **Data Processing**: Pandas, PyArrow

## 📦 Installation & Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
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
   export CLICKHOUSE_HOST="localhost"
   export CLICKHOUSE_USER="default"
   export CLICKHOUSE_PASSWORD=""
   export KAFKA_SECURITY_PROTOCOL="PLAINTEXT"
   ```

## 🚀 Usage

### Running the Data Pipeline

1. **Start the Kafka Producer** (generates and sends data)
   ```bash
   python src/kafka/producer.py --batch_size 1000 --time_interval 1 --data_generation_speed 10000
   ```

2. **Start the Kafka Consumer** (consumes and stores data in ClickHouse)
   ```bash
   python src/kafka/consumer.py
   ```

3. **Launch the Analytics Dashboard**
   ```bash
   streamlit run src/clickhouse/clickhouse_dashboard.py
   ```

### Configuration Options

#### Producer Parameters
- `--batch_size`: Number of records per batch (default: 1000)
- `--time_interval`: Time interval between batches in seconds (default: 1)
- `--data_generation_speed`: Speed multiplier for data generation (default: 10000)

#### Data Schema
The generated clickstream data includes:
- `user_id`: Unique user identifier (user_0000 to user_9998)
- `item_id`: Product/item identifier (item_0000 to item_0049) 
- `interaction_type`: Type of interaction (click, view, purchase)
- `timestamp`: Event timestamp

## 📊 Dashboard Features

The Streamlit dashboard provides real-time analytics including:

- **Key Metrics**: Total interactions, unique users, unique items
- **Interaction Breakdown**: Distribution of clicks, views, and purchases
- **Time Series Analysis**: Trends over time
- **User Behavior Analytics**: Top users and items
- **Real-time Updates**: Auto-refreshing data every 30 seconds

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Test Kafka components
python test/kafka_producer.py
python test/kafka_consumer.py

# Test database connections
python test/test_clickhouse.py
python test/test_druid.py
python test/test_mongo_db.py
```

## 📁 Project Structure

```
avrioc_case_study/
├── docker-compose.yml          # Kafka container setup
├── requirements.txt            # Python dependencies
├── src/
│   ├── kafka/
│   │   ├── data_generator.py   # Clickstream data generation
│   │   ├── producer.py         # Kafka producer implementation
│   │   └── consumer.py         # Kafka consumer with ClickHouse integration
│   └── clickhouse/
│       └── clickhouse_dashboard.py  # Streamlit analytics dashboard
└── test/
    ├── kafka_producer.py       # Producer tests
    ├── kafka_consumer.py       # Consumer tests
    ├── test_clickhouse.py      # ClickHouse tests
    ├── test_druid.py          # Druid tests
    └── test_mongo_db.py       # MongoDB tests
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `KAFKA_BROKER_URL` | Kafka broker connection string | `localhost:9092` |
| `KAFKA_TOPIC` | Kafka topic name | `clickstream_topic` |
| `CLICKHOUSE_HOST` | ClickHouse server host | `localhost` |
| `CLICKHOUSE_USER` | ClickHouse username | `default` |
| `CLICKHOUSE_PASSWORD` | ClickHouse password | `` |
| `KAFKA_SECURITY_PROTOCOL` | Kafka security protocol | `PLAINTEXT` |

## 🐛 Troubleshooting

### Common Issues

1. **Kafka Connection Error**
   - Ensure Docker containers are running: `docker-compose ps`
   - Check Kafka broker URL and port accessibility

2. **ClickHouse Connection Error**
   - Verify ClickHouse server is running and accessible
   - Check connection parameters and credentials

3. **Dashboard Not Loading**
   - Ensure Streamlit is installed: `pip install streamlit`
   - Check that ClickHouse contains data

### Logs and Monitoring

- View Kafka logs: `docker-compose logs kafka`
- Monitor topic: `docker exec -it <kafka-container> kafka-topics --list --bootstrap-server localhost:9092`

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
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Note**: This is a demonstration project for educational and case study purposes. For production use, additional security, monitoring, and error handling should be implemented.
