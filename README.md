# airflow
data pipeline for crawling 

### DAGs
#### linkareer_cover_letter_dag
- 링커리어 웹페이지 크롤링 > S3 에 .csv 로 load > VectorDB 로 벡터라이징 
- daily batch , 오전 9시 이전에 작업 완료 가능하도록 스케줄링 

#### cleanup_metadata_dag

- 매일 실행되어 30일 이전의 airflow metadata 를 불필요하다고 판단하여, 주기적으로 정리 작업 실행. 

### Monitoring 

#### Prometheus & Grafana 
- Airflow 메트릭 모니터링을 위해 프로메테우스와 그라파나 선정 