# Tracking LUMA Energy Outages

## Requirements

- Python 3.6+

## Getting started

```
# Setup virtualenv
$ make init

# Install all dependencies
$ make install

# Run scraping process
$ make run-scrape

# Run datasette
$ make run-datasette
```

## Data sources

- https://api.miluma.lumapr.com/miluma-outage-api/outage/regionsWithoutService
- https://api.miluma.lumapr.com/miluma-outage-api/outage/municipality/towns
