<template>
  <div style="display: flex;">
    <div id="upBar" style="width: 50%; height: 600px;"></div>
    <div id="upPie" style="width: 50%; height: 600px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import Papa from 'papaparse';
import { addLine } from '../utils';

export default {
  name: 'PopularUpData',
  data() {
    return {
      upData: [],
    };
  },
  methods: {
    drawCharts() {
      const upNames = this.upData.map(item => addLine(item.up, 2));
      const times = this.upData.map(item => parseInt(item.popular_up_times));

      // 优化后的配色
      const colors = [
        '#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F',
        '#EDC949', '#AF7AA1', '#FF9DA7', '#9C755F', '#BAB0AC',
      ];

      // 柱状图配置
      const barChart = echarts.init(document.getElementById('upBar'));
      const barOption = {
        title: {
          text: '上榜次数前十的UP主',
          left: 'center',
          textStyle: {
            fontSize: 22,
            fontWeight: 'bold',
            color: '#333',
          },
        },
        xAxis: {
          type: 'category',
          data: upNames,
          axisLabel: {
            fontSize: 12,
            color: '#666',
            interval: 0,
            formatter: value => {
              // 自动换行以防止名称过长
              const maxLineLength = 6;
              return value.length > maxLineLength
                ? value.match(new RegExp(`.{1,${maxLineLength}}`, 'g')).join('\n')
                : value;
            },
          },
          axisLine: { lineStyle: { color: '#999' } },
        },
        yAxis: {
          type: 'value',
          axisLabel: { fontSize: 12, color: '#666' },
          splitLine: { lineStyle: { type: 'dashed', color: '#ddd' } },
        },
        tooltip: {
          trigger: 'item',
          backgroundColor: '#fff',
          borderColor: '#ccc',
          borderWidth: 1,
          textStyle: { color: '#000' },
          formatter: params => `
            <div style="text-align: left;">
              <b>${params.name}</b><br/>
              <span style="color: #888;">上榜次数: </span>${params.value}
            </div>
          `,
        },
        series: [
          {
            data: times,
            type: 'bar',
            label: {
              show: true,
              position: 'top',
              color: '#333',
              fontSize: 12,
            },
            itemStyle: {
              color: (params) => colors[params.dataIndex % colors.length],
            },
          },
        ],
        grid: { left: '10%', right: '10%', bottom: '15%' },
      };
      barChart.setOption(barOption);

      // 饼图配置
      const pieChart = echarts.init(document.getElementById('upPie'));
      const pieOption = {
        title: {
          text: '上榜次数前十的UP主占比',
          left: 'center',
          textStyle: {
            fontSize: 22,
            fontWeight: 'bold',
            color: '#333',
          },
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)',
        },
        legend: {
          bottom: 10,
          left: 'center',
          itemWidth: 14,
          itemHeight: 14,
          textStyle: { fontSize: 12, color: '#666' },
        },
        series: [
          {
            type: 'pie',
            radius: ['30%', '55%'],
            center: ['50%', '50%'],
            data: this.upData.map((item, index) => ({
              name: item.up,
              value: parseInt(item.popular_up_times),
              itemStyle: {
                color: colors[index % colors.length], // 饼图颜色与柱状图一致
              },
            })),
            label: {
              position: 'outside',
              formatter: '{b}: {c} ({d}%)', // 完整显示数据
              fontSize: 12,
            },
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
          },
        ],
      };
      pieChart.setOption(pieOption);
    },
  },
  mounted() {
    axios.get('/static/top_popular_up.csv').then(response => {
      Papa.parse(response.data, {
        header: true,
        complete: results => {
          this.upData = results.data.filter(item => item.up);
          this.drawCharts();
        },
      });
    });
  },
};
</script>

<style scoped>
#upBar,
#upPie {
  margin-bottom: 60px;
}
</style>
