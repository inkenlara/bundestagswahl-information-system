import React, { useState, useEffect } from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

import { Pie } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

const PieChartq1 = () => {
  const [data, setData] = useState([]);
  const getData = () => {
    fetch("http://localhost:8000/query1_chart")
      .then(function (response) {
        console.log(response);
        return response.json();
      })
      .then(function (myJson) {
        console.log(myJson);
        setData(myJson);
      });
  };
  useEffect(() => {
    getData();
  }, []);
  var options = {
    maintainAspectRatio: false,
    scales: {},
    legend: {
      labels: {
        fontSize: 25,
      },
    },
  };

  var vals = {
    labels: Object.keys(data),
    datasets: [
      {
        // csu, cdu, linke, fdp, spd, grune, afd, ssw
        label: "Anzahl Sitze",
        data: Object.values(data),
        backgroundColor: [
          "rgba(0, 0, 153, 0.2)",
          "rgba(0, 0, 0, 0.2)",
          "rgba(255, 0, 153, 0.2)",
          "rgba(238, 255, 0, 0.2)",
          "rgba(222, 78, 97, 0.2)",
          "rgba(30, 252, 10, 0.2)",
          "rgba(0, 153, 255, 0.2)",
          "rgba(0, 26, 219, 0.2)",
        ],
        borderColor: [
          "rgba(0, 0, 153, 1)",
          "rgba(0, 0, 0, 1)",
          "rgba(255, 0, 153, 1)",
          "rgba(238, 255, 0, 1)",
          "rgba(222, 78, 97, 1)",
          "rgba(30, 252, 10, 1)",
          "rgba(0, 153, 255, 1)",
          "rgba(0, 26, 219, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div>
      <Pie data={vals} height={400} options={options} />
    </div>
  );
};

export default PieChartq1;
