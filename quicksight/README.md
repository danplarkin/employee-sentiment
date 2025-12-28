# QuickSight Dashboard Configuration

This directory contains configuration for the Employee Sentiment QuickSight dashboard.

## Setup Instructions

1. **Create Athena Table** to query DynamoDB:
   ```sql
   CREATE EXTERNAL TABLE sentiment_results (
     feedback_id string,
     employee_id string,
     department string,
     feedback_text string,
     timestamp bigint,
     sentiment string,
     sentiment_scores struct<
       positive:double,
       negative:double,
       neutral:double,
       mixed:double
     >
   )
   STORED BY 'com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory'
   LOCATION 'dynamodb://employee-sentiment-results-dev'
   TBLPROPERTIES (
     "dynamodb.table.name" = "employee-sentiment-results-dev",
     "dynamodb.column.mapping" = "feedback_id:feedback_id,employee_id:employee_id,department:department,feedback_text:feedback_text,timestamp:timestamp,sentiment:sentiment,sentiment_scores:sentiment_scores"
   );
   ```

2. **Create QuickSight Data Source**:
   - Navigate to QuickSight console
   - Create new data source from Athena
   - Select the `sentiment_results` table

3. **Build Dashboard with these visualizations**:
   - **Sentiment Distribution** (Pie Chart): Count by sentiment (Positive, Negative, Neutral, Mixed)
   - **Sentiment Trend Over Time** (Line Chart): Count of feedback by sentiment over time
   - **Department Sentiment** (Stacked Bar Chart): Sentiment breakdown by department
   - **Sentiment Score Heatmap** (Table): Average sentiment scores by department
   - **Recent Negative Feedback** (Table): Latest negative feedback entries for review

4. **Key Metrics to Display**:
   - Total Feedback Count
   - Average Positive Score
   - Negative Feedback Percentage
   - Most Common Sentiment

## Dashboard Layout

```
┌─────────────────────────────────────────────────────┐
│           Employee Sentiment Dashboard              │
├──────────────┬──────────────┬──────────────────────┤
│ Total        │ Avg Positive │ Negative %           │
│ Feedback:    │ Score:       │                      │
│ 1,234        │ 0.78         │ 15%                  │
├──────────────┴──────────────┴──────────────────────┤
│                                                     │
│  Sentiment Distribution        Trend Over Time     │
│  (Pie Chart)                   (Line Chart)        │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Sentiment by Department       Sentiment Scores    │
│  (Stacked Bar)                 (Heatmap)          │
│                                                     │
├─────────────────────────────────────────────────────┤
│  Recent Negative Feedback                          │
│  (Table with details)                              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Filters

- Date Range
- Department
- Sentiment Type
- Employee ID (optional)
