# Retail sales findings

Generated from the cleaned UCI Online Retail dataset. Values describe this dataset only.

## Key results

- **Net revenue:** £9,748,131.07 across **20,726 completed orders**.
- **Average order value:** £513.47 (revenue from
  non-cancellation invoices, including their return adjustments, divided by
  completed orders).
- **Largest country by net revenue:** United Kingdom at £8,189,252.30
  (84.0% of net revenue).
- **Highest-revenue month:** 2011-11 at £1,456,145.80.
- **Top product by net revenue:** DOTCOM POSTAGE (stock code DOT)
  at £206,245.48.
- **Return rows retained:** 1,336, totaling £0.00
  in revenue. The source does not provide return reasons.
- **Cancellation rows retained:** 9,251. They are excluded from
  completed-order counts and remain in net-revenue calculations.

## Suggested actions

1. Review performance by country before allocating growth effort. The largest
   country accounts for 84.0% of net revenue; validate that
   concentration against current sales before making investment decisions.
2. Review the leading products' availability and customer feedback. The dataset
   contains no inventory or cost data, so it cannot establish stock shortages
   or product profitability.
3. Investigate negative-quantity and cancellation activity using operational
   records with return reasons; those reasons are not present in this dataset.
4. Treat monthly differences as descriptive. The dataset covers about one year
   and includes a partial December, so it is not enough to establish a reliable
   seasonal pattern or forecast.

## Data preparation summary

| Check | Rows |
|---|---:|
| Source rows | 541,909 |
| Exact duplicates removed | 5,268 |
| Invalid rows removed | 2 |
| Clean rows retained | 536,639 |
| Missing customer IDs retained | 135,035 |
| Outlier rows flagged, not removed | 64,871 |

## Limitations

This is historical transaction data for one retailer, not a representative
retail market sample. It contains no cost, profit, product category, inventory,
marketing, return-reason, or customer-demographic fields. Revenue must not be
presented as profit, and correlation or month-to-month changes do not establish
causation.
