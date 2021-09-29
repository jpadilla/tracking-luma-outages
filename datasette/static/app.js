function fetchData() {
  return fetch("/data/affected_customers_by_region_and_date.json").then(
    function (response) {
      if (response.status >= 400) {
        throw new Error("Bad response from server");
      }
      return response.json();
    }
  );
}

function generateChart() {
  return bb.generate({
    zoom: {
      enabled: true,
      type: "drag"
    },
    data: {
      x: "x",
      columns: [],
      type: "line",
    },
    axis: {
      y: {
        tick: {
          format: function(d) {
            return d + "%";
          }
        }
      },
      x: {
        type: "timeseries",
        tick: {
          format: "%Y-%m-%d %H:%M",
        },
      },
    },
    title: {
      text: "% Clientes Sin Servicio por día",
    },
    bindto: "#timeseriesChart",
  });
}

document.addEventListener("DOMContentLoaded", function () {
  let chart = generateChart();

  fetchData().then(function (data) {
    let results = data.rows.map(function (row) {
      let rowObj = data.columns.reduce(function (prev, val, idx) {
        prev[val] = row[idx];
        return prev;
      }, {});
      rowObj.value = rowObj.affected_customers / rowObj.total_customers;
      return rowObj;
    });

    let dates = results.map(function (r) {
      return r.date;
    });
    let regions = results.map(function (r) {
      return r.region;
    });
    let uniqueDates = Array.from(new Set(dates));
    let uniqueRegions = Array.from(new Set(regions));
    let columns = [
      ["x"].concat(uniqueDates.map(function(d) { return new Date(d); })),
    ].concat(
      uniqueRegions.map(function (region) {
          return [region].concat(
            results
              .filter(function (r) {
                return r.region === region;
              })
              .map(function (r) {
                return r.value;
              })
          );
        })
    )

    chart.load({
      columns: columns,
    });
  });
});
