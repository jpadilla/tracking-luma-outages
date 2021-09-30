function fetchData(path) {
  return fetch(path).then(function (response) {
    if (response.status >= 400) {
      throw new Error('Bad response from server');
    }
    return response.json();
  });
}

function generateAffectedCustomersChart() {
  let chart = bb.generate({
    zoom: {
      enabled: true,
      type: 'drag',
    },
    data: {
      x: 'x',
      columns: [],
      type: 'line',
    },
    axis: {
      y: {
        min: 0,
      },
      x: {
        type: 'timeseries',
        tick: {
          format: '%Y-%m-%d %I %p',
        },
      },
    },
    title: {
      text: 'Total de clientes sin servicio',
    },
    bindto: '#chart-affected-customers-by-date',
  });

  return fetchData('/data/affected_customers_by_region_and_date.json').then(
    function (data) {
      let results = data.rows.map(function (row) {
        let rowObj = data.columns.reduce(function (prev, val, idx) {
          prev[val] = row[idx];
          return prev;
        }, {});
        return rowObj;
      });

      let dates = results.map(function (r) {
        return r.date;
      });
      let regions = results.map(function (r) {
        return r.region;
      });
      let uniqueDates = Array.from(new Set(dates)).map(function (d) {
        return new Date(d);
      });
      let uniqueRegions = Array.from(new Set(regions));
      let columns = [['x'].concat(uniqueDates)].concat(
        uniqueRegions.map(function (region) {
          return [region].concat(
            results
              .filter(function (r) {
                return r.region === region;
              })
              .map(function (r) {
                return r.affected_customers;
              })
          );
        })
      );

      chart.load({
        columns: columns,
      });
    }
  );
}

function generateTotalOutagesChart() {
  let chart = bb.generate({
    zoom: {
      enabled: true,
      type: 'drag',
    },
    data: {
      x: 'x',
      columns: [],
      type: 'line',
    },
    axis: {
      y: {
        min: 0,
      },
      x: {
        type: 'timeseries',
        tick: {
          format: '%Y-%m-%d %I %p',
        },
      },
    },
    title: {
      text: 'Total de sectores sin servicio',
    },
    bindto: '#chart-outages-by-date',
  });

  return fetchData('/data/outages_by_date.json').then(function (data) {
    let results = data.rows.map(function (row) {
      let rowObj = data.columns.reduce(function (prev, val, idx) {
        prev[val] = row[idx];
        return prev;
      }, {});
      return rowObj;
    });

    let dates = results.map(function (r) {
      return r.date;
    });
    let uniqueDates = Array.from(new Set(dates)).map(function (d) {
      return new Date(d);
    });
    let columns = [['x'].concat(uniqueDates)].concat([
      ['sectores'].concat(
        results.map(function (r) {
          return r.count;
        })
      ),
    ]);

    chart.load({
      columns: columns,
    });
  });
}

document.addEventListener('DOMContentLoaded', function () {
  generateAffectedCustomersChart();
  generateTotalOutagesChart();
});
