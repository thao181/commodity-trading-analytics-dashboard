# Commodity Trading and Market Analytics Dashboard

## Project Overview

This project demonstrates an end-to-end analytics workflow that integrates external commodity market data with simulated internal trading, finance and position datasets.

The objective was to develop a reusable Power BI reporting solution that supports monthly data updates and provides stakeholders with visibility into:

- commodity trading activity;
- buy and sell contract values;
- traded volume;
- settlement status;
- cash flow movement;
- commodity positions;
- daily, weekly and monthly performance.

The project also includes a business-friendly metric and chart dictionary so that non-technical stakeholders can understand how each KPI is calculated and how each dashboard visual should be interpreted.

---

## Business Scenario

Commodity trading teams commonly rely on both external market information and internal operational data.

External data provides information about commodity market prices, while internal systems contain trading transactions, settlement activity, cash movement and reported positions.

Because real internal trading data is commercially sensitive, synthetic internal datasets were generated using Python to simulate a realistic reporting environment without exposing confidential company information.

---

## Project Workflow

### 1. External Market Data Preparation

Commodity market data was sourced from the World Bank.

Power Query was used to:

- import the source data;
- clean and standardise the dataset;
- remove unnecessary fields;
- retain relevant commodities and reporting periods;
- correct data types;
- create reusable transformation steps.

The Power Query workflow was designed to support recurring monthly updates.

When a new monthly source file becomes available, the existing source file can be replaced and Power Query will automatically apply the previously configured transformation steps.

This reduces manual data preparation and creates a more consistent reporting process.

---

### 2. Synthetic Internal Data Generation

Python was used to generate simulated internal datasets representing common commodity trading operations.

The generated datasets include:

#### Trading Data

Contains simulated commodity transactions, including:

- trade ID;
- trade date;
- commodity;
- transaction type;
- traded volume;
- contract price.

Transaction types include:

- Buy;
- Sell.

#### Finance Data

Contains simulated settlement and cash flow information, including:

- cash ID;
- trade ID;
- settlement date;
- cash flow type;
- settlement amount;
- settlement status.

Settlement statuses include:

- Settled;
- Pending.

#### Position Data

Contains simulated commodity position records, including:

- reporting date;
- commodity;
- reported position;
- long or short market exposure.

All synthetic datasets were created solely for portfolio and demonstration purposes.

---

### 3. Data Transformation and Integration

Power Query was used to clean, transform and integrate the external World Bank data with the simulated internal datasets.

The transformation process included:

- standardising commodity names;
- converting columns to appropriate data types;
- handling missing values;
- validating dates and identifiers;
- merging trading and finance records;
- integrating market price information;
- creating reporting month fields;
- preparing the final analytical dataset.

The main reporting table combines information related to:

- trading activity;
- contract prices;
- market prices;
- traded volume;
- settlement activity;
- cash flow;
- commodity positions.

---

### 4. Power BI Data Model and Dashboard Development

The transformed datasets were loaded into Power BI to create the analytical model.

DAX measures were developed to calculate key reporting metrics, while custom SVG measures were used to create visually consistent dashboard components.

The dashboard was designed using a dark teal corporate theme with interactive filters for:

- reporting year;
- reporting month;
- commodity;
- settlement status;
- cash flow type.

---

## Dashboard Pages and Visuals

### Executive Overview

Provides a high-level summary of commodity trading performance.

Key visuals include:

- Monthly Trade Notional;
- Buy versus Sell Volume;
- Trade Notional by Commodity;
- Latest Position by Commodity;
- Volume Share by Commodity.

---

### Monthly Commodity Trading Report

Provides detailed analysis of activity during the selected reporting month.

The page includes:

- KPI summary cards;
- Monthly Performance Summary;
- Daily Trade Notional;
- Monthly Trade Statistics;
- Cumulative Net Cash Flow;
- Weekly Performance.

---


```text
Total Trade Notional = Traded Volume × Contract Price
