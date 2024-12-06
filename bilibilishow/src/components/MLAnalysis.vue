<template>
  <div>
    <div id="heatmap" class="chart-container"></div>
    <div id="comparisonBar" class="chart-container"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import Papa from 'papaparse';

export default {
  name: 'Visualization',
  data() {
    return {
      variables: [], // Feature names for the heatmap
      corMatrix: [], // Correlation matrix data
      comparisonData: [], // Performance data for classifiers
    };
  },
  methods: {
    drawHeatmap() {
      // Prepare heatmap data
      const heatmapData = [];
      for (let i = 0; i < this.variables.length; i++) {
        for (let j = 0; j < this.variables.length; j++) {
          heatmapData.push([i, j, parseFloat(this.corMatrix[i][j])]);
        }
      }

      // Configure the heatmap chart
      const heatmapChart = echarts.init(document.getElementById('heatmap'));
      const heatmapOption = {
        title: {
          text: '自变量相关性',
          left: 'center',
          textStyle: { fontSize: 20, fontWeight: 'bold' },
        },
        tooltip: {
          trigger: 'item',
          formatter: params =>
            `相关性 (${this.variables[params.value[0]]} - ${this.variables[params.value[1]]}): ${params.value[2].toFixed(2)}`,
        },
        xAxis: {
          type: 'category',
          data: this.variables,
          name: 'Features',
          nameTextStyle: { fontSize: 14, fontWeight: 'bold' },
          axisLabel: { fontSize: 12, fontWeight: 'bold' },
        },
        yAxis: {
          type: 'category',
          data: this.variables,
          name: 'Features',
          nameTextStyle: { fontSize: 14, fontWeight: 'bold' },
          axisLabel: { fontSize: 12, fontWeight: 'bold' },
        },
        visualMap: {
          min: 0,
          max: 1,
          calculable: true,
          orient: 'vertical',
          right: '5%',
          top: '15%',
          inRange: { color: ['#42A5F5', '#FFEB3B', '#FF7043'] }, // Blue to red gradient
        },
        series: [
          {
            type: 'heatmap',
            data: heatmapData,
            label: {
              show: true,
              formatter: params => params.value[2].toFixed(2),
              fontSize: 14,
              fontWeight: 'bold',
              color: '#000',
            },
            emphasis: {
              itemStyle: {
                borderColor: '#000',
                borderWidth: 1,
              },
            },
          },
        ],
      };
      heatmapChart.setOption(heatmapOption);
    },
    drawComparisonBar() {
      const classifiers = this.comparisonData.map(item => item.classifier);
      const acc = this.comparisonData.map(item => parseFloat(item.Acc));
      const auc = this.comparisonData.map(item => parseFloat(item.Auc));

      const barChart = echarts.init(document.getElementById('comparisonBar'));
      const barOption = {
        title: {
          text: '不同分类器的性能比较',
          left: 'center',
          textStyle: { fontSize: 20, fontWeight: 'bold' },
        },
        tooltip: {
          trigger: 'item',
          formatter: params =>
            `${params.seriesName} (${params.name}): ${params.value.toFixed(3)}`,
        },
        xAxis: {
          type: 'category',
          data: classifiers, // Only 4 classifiers, no extra empty column
          name: 'Classifiers',
          nameTextStyle: { fontSize: 16, fontWeight: 'bold' },
          axisLabel: { rotate: 0, fontSize: 14, fontWeight: 'bold' },
        },
        yAxis: {
          type: 'value',
          name: 'Performance',
          nameTextStyle: { fontSize: 16, fontWeight: 'bold' },
          axisLabel: { fontSize: 14 },
        },
        legend: {
          data: ['Acc', 'Auc'],
          left: 'center',
          top: '10%',
        },
        series: [
          {
            name: 'Acc',
            data: acc,
            type: 'bar',
            itemStyle: { color: '#FF7043' },
          },
          {
            name: 'Auc',
            data: auc,
            type: 'bar',
            itemStyle: { color: '#42A5F5' },
          },
        ],
      };
      barChart.setOption(barOption);
    },
  },
  mounted() {
    // Load heatmap data
    axios.get('/static/cor_matrix.csv').then(response => {
      Papa.parse(response.data, {
        header: false,
        dynamicTyping: true,
        complete: results => {
          const rawData = results.data;
          this.variables = ['view', ...rawData[0].slice(1)]; // Add 'view' as the first variable
          this.corMatrix = rawData.slice(1).map((row, index) => {
            return [parseFloat(row[0]), ...row.slice(1).map(value => parseFloat(value || 0))];
          });
          this.drawHeatmap();
        },
      });
    });

    // Load comparison bar chart data
    axios.get('/static/comparison.csv').then(response => {
      Papa.parse(response.data, {
        header: true,
        complete: results => {
          this.comparisonData = results.data.filter(item => item.classifier); // Remove empty rows
          this.drawComparisonBar();
        },
      });
    });
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 600px;
  margin-bottom: 60px;
  padding: 10px;
  border-radius: 10px;
  background: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
