<template>
  <div style="display: flex;">
    <div id="subjectBar" style="width: 50%; height: 600px;"></div>
    <div id="subjectPie" style="width: 50%; height: 600px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import Papa from 'papaparse';
import { addLine } from '../utils';

export default {
  name: 'PopularSubjectData',
  data() {
    return {
      subjectData: [],
    };
  },
  methods: {
    drawCharts() {
      const subjects = this.subjectData.map(item => addLine(item.tname, 2));
      const times = this.subjectData.map(item => parseInt(item.popular_subject_times));

      // 更新后的配色
      const colors = [
        '#5470C6', '#91CC75', '#EE6666', '#FAC858', '#73C0DE',
        '#3BA272', '#FC8452', '#9A60B4', '#EA7CCC', '#FFA07A',
      ];

      // 柱状图配置
      const barChart = echarts.init(document.getElementById('subjectBar'));
      const barOption = {
        title: {
          text: '上榜次数前十的话题',
          left: 'center',
          textStyle: {
            fontSize: 22,
            fontWeight: 'bold',
            color: '#333',
          },
        },
        xAxis: {
          type: 'category',
          data: subjects,
          axisLabel: {
            fontSize: 12,
            color: '#666',
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
            label: { show: true, position: 'top', color: '#333', fontSize: 12 },
            itemStyle: {
              color: (params) => colors[params.dataIndex % colors.length],
            },
          },
        ],
        grid: { left: '10%', right: '10%', bottom: '15%' },
      };
      barChart.setOption(barOption);

      // 饼图配置
      const pieChart = echarts.init(document.getElementById('subjectPie'));
      const pieOption = {
        title: {
          text: '上榜次数前十的话题占比',
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
        series: [
          {
            type: 'pie',
            radius: ['30%', '55%'],
            center: ['50%', '50%'],
            data: this.subjectData.map((item, index) => ({
              name: item.tname,
              value: parseInt(item.popular_subject_times),
              itemStyle: {
                color: colors[index % colors.length], // 饼图颜色与柱状图一致
              },
            })),
            label: {
              position: 'outside',
              formatter: '{b}: {c} ({d}%)', // 显示完整数据
              fontSize: 12,
            },
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
          },
        ],
        legend: {
          bottom: 10,
          left: 'center',
          itemWidth: 14,
          itemHeight: 14,
          textStyle: { fontSize: 12, color: '#666' },
        },
      };
      pieChart.setOption(pieOption);
    },
  },
  mounted() {
    axios.get('/static/top_popular_subject.csv').then(response => {
      Papa.parse(response.data, {
        header: true,
        complete: results => {
          this.subjectData = results.data.filter(item => item.tname);
          this.drawCharts();
        },
      });
    });
  },
};
</script>

<style scoped>
#subjectBar,
#subjectPie {
  margin-bottom: 60px;
}
</style>
