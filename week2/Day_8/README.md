# 🐼 Advanced Pandas Journey

## 🎯 Goal

Master Pandas beyond basic syntax by understanding its internal reasoning, predicting outputs before execution, and developing the ability to perform real-world EDA and feature engineering independently.

---

# ✅ Day 1 — Advanced Data Manipulation

## Indexing & Selection

- Advanced `loc[]`
- Advanced `iloc[]`
- Boolean Indexing
- Multiple Conditions
- Operator Precedence (`&`, `|`, `~`)
- Proper use of Parentheses

---

## Filtering

- Complex Filtering
- `isin()`
- `between()`
- `query()`
- `where()`
- `mask()`

---

## Sorting

- `sort_values()`
- Multi-column Sorting
- Ascending vs Descending
- Stable Sorting Concepts

---

## Handling Missing Values

- `isna()`
- `notna()`
- `dropna()`
- `fillna()`
- Understanding NaN behaviour

---

## Column Creation

- Creating New Columns
- Conditional Columns
- `np.where()`
- `np.select()`

---

## Mapping & Replacement

- `map()`
- `replace()`

---

## Feature Engineering

- Building new features
- Business logic columns
- Rule-based categorisation

---

## Transform

Mental Model:

Rows remain the same.

Each row receives information calculated from its own group.

Applications:

- Department Average Salary
- Department Average Projects
- Percentage calculations
- Group statistics per row

---

## Core Concepts Learned

- Difference between Filtering and Transformation
- Difference between Aggregation and Transformation
- Thinking in DataFrames instead of loops

---

# ✅ Day 2 — GroupBy & Aggregation

## GroupBy

Understanding:

Split → Apply → Combine

Learned:

- DataFrameGroupBy
- SeriesGroupBy
- Group objects
- Internal grouping mechanism

---

## Counting

Difference between:

- `size()`
- `count()`

Understanding:

- Counting rows
- Counting non-null values

---

## Aggregation

Understanding:

- What aggregation actually means
- Why aggregation shrinks data
- Statistical summaries
- Business summaries

---

## The `agg()` Function

Learned:

- Philosophy behind `agg()`
- Why it exists
- Why it is called an orchestrator
- Difference between:

```python
.mean()
```

and

```python
.agg("mean")
```

---

## Different Forms of Aggregation

- Single aggregation
- Multiple aggregations
- Dictionary aggregation
- Named Aggregation

---

## MultiIndex Columns

Reasoning behind:

- Why they exist
- When Pandas creates them
- When Pandas avoids them

Golden Rule:

> MultiIndex columns appear only when an original column produces multiple aggregation results.

---

## Named Aggregation

Advantages:

- Readable outputs
- Cleaner reports
- Dashboard-ready summaries
- Better feature engineering

---

## Prediction Practice

Before executing every operation, predict:

- Input Object
- Operation Type
- Return Type
- Shape
- Index
- Columns
- Row Count
- MultiIndex Behaviour

This developed intuition instead of memorisation.

---

# 🧠 Important Mental Models Built

## Aggregation

Many rows

↓

One summary

---

## Transformation

Many rows

↓

Same number of rows

↓

New information added

---

## GroupBy

Split

↓

Apply

↓

Combine

---

## `agg()`

Not a statistical function.

It is an **orchestrator** that coordinates one or more aggregation functions and combines the results into a structured summary.

---

# 📌 Current Progress

✅ Advanced Filtering

✅ Boolean Logic

✅ Feature Engineering

✅ Missing Value Handling

✅ Sorting

✅ Transform

✅ GroupBy

✅ Aggregation

✅ MultiIndex Reasoning

✅ Named Aggregation

---

# 🔜 Next Topics

- `apply()`
- `filter()` on groups
- Advanced `transform()`
- Method Chaining
- `pipe()`
- Merge Mastery
- Join vs Merge vs Concat
- Pivot Tables
- Crosstab
- MultiIndex Operations
- Window Functions
- Time Series Operations
- Performance Optimisation
- Real-world EDA Challenges

---

# 🚀 Final Goal

By the end of this journey, I aim to:

- Predict Pandas outputs before execution.
- Perform complete exploratory data analysis independently.
- Engineer meaningful features for ML pipelines.
- Write clean, readable, and efficient Pandas code.
- Understand the reasoning behind Pandas APIs instead of memorising syntax.
- Transition confidently into advanced machine learning workflows.
