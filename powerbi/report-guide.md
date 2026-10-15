# Power BI report guide

## Load and model

1. Generate `data/processed/retail_sales_clean.csv` by following the root
   README's Quick start.
2. In Power BI Desktop, select **Get data → Text/CSV** and load the CSV.
3. Confirm `invoice_date` is Date/Time, `invoice_month` is text, numeric fields
   are numeric, and the `is_*` / `*_outlier` fields are Boolean.
4. Create the measures in `measures.dax`.
5. Format `Net Revenue`, `Average Order Value`, and `Return Revenue` as currency.
   Use a date hierarchy on `invoice_date` or `invoice_month` for time visuals.

## Suggested pages

- **Overview:** cards for Net Revenue, Completed Orders, and Average Order
  Value; a line chart of monthly Net Revenue; country and date slicers.
- **Products and countries:** bar charts for net revenue by product description
  and country. Use stock code as a tooltip or drill-through key.
- **Returns and quality:** cards for Return Rows and Flagged Outlier Rows; a
  table filtered by `is_return` or `is_outlier`.

## Metric definitions

- Net revenue is quantity × unit price summed across retained rows, so negative
  quantities reduce revenue.
- Completed Orders counts distinct, non-cancellation invoices with positive
  quantity.
- Average Order Value is revenue on non-cancellation invoices (including
  transaction-level return adjustments) divided by completed orders. The source
  does not link return records to a separate original-order key, so this is
  descriptive rather than cohort-adjusted.
- The source has no cost or category columns. Do not label revenue as profit or
  assign inferred product categories.
