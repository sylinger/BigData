<template>
  <div>
    <div id="videoBar" style="width: 1200px; height: 600px;"></div>
    <div id="upBar" style="width: 1200px; height: 600px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import Papa from 'papaparse';
import { addLine } from '../utils';

export default {
  name: 'LikeData',
  data() {
    return {
      videoData: [],
      upData: [],
    };
  },
  methods: {
    drawCharts() {
      const videoTitles = this.videoData.map(item => addLine(item.title));
      const videoLikes = this.videoData.map(item => parseInt(item.like_data));

      const gradientColor = {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [
          { offset: 0, color: '#A6FFCB' }, // 顶部颜色
          { offset: 1, color: '#12D8FA' }, // 底部颜色
        ],
      };

      const videoBarChart = echarts.init(document.getElementById('videoBar'));
      const videoBarOption = {
        title: {
          text: 'Top10点赞数最多的视频',
          left: 'center',
          top: '5%',
          textStyle: {
            fontSize: 26,
            fontWeight: 'bold',
            color:'#12D8DF'
          },
        },
        xAxis: {
          type: 'category',
          data: videoTitles,
          axisLabel: {
            rotate: 0, // 不旋转
            fontSize: 12,
            color: '#333',
            interval: 0, // 强制显示所有标签
            //formatter: value => (value.length > 10 ? value.slice(0, 10) + '...' : value),
          },
          axisLine: { lineStyle: { color: '#999' } },
        },
        yAxis: {
          type: 'value',
          axisLabel: { fontSize: 12, color: '#333' },
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
              <span style="color: #888;">点赞数: </span>${params.value}
            </div>
          `,
        },
        series: [
          {
            data: videoLikes,
            type: 'bar',
            label: { show: true, position: 'top', color: '#333', fontSize: 12 },
            itemStyle: {
              color: gradientColor,
            },
          },
        ],
        grid: { left: '10%', right: '10%', bottom: '15%' },
      };
      videoBarChart.setOption(videoBarOption);

      const upNames = this.upData.map(item => addLine(item.up));
      const upLikes = this.upData.map(item => parseInt(item.like_data));

      const upBarChart = echarts.init(document.getElementById('upBar'));
      const upBarOption = {
        title: {
          text: 'Top10点赞数最多的UP主',
          left: 'center',
          top: '5%',
          textStyle: {
            fontSize: 26,
            fontWeight: 'bold',
            color:'#12D8DF'
          },
        },
        xAxis: {
          type: 'category',
          data: upNames,
          axisLabel: {
            rotate: 0,
            fontSize: 12,
            color: '#333',
            interval: 0,
            //formatter: value => (value.length > 10 ? value.slice(0, 10) + '...' : value),
          },
          axisLine: { lineStyle: { color: '#999' } },
        },
        yAxis: {
          type: 'value',
          axisLabel: { fontSize: 12, color: '#333' },
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
              <span style="color: #888;">点赞数: </span>${params.value}
            </div>
          `,
        },
        series: [
          {
            data: upLikes,
            type: 'bar',
            label: { show: true, position: 'top', color: '#333', fontSize: 12 },
            itemStyle: {
              color: gradientColor,
            },
          },
        ],
        grid: { left: '10%', right: '10%', bottom: '15%' },
      };
      upBarChart.setOption(upBarOption);
    },
  },
  mounted() {
    axios.get('/static/video_like_data.csv').then(response => {
      Papa.parse(response.data, {
        header: true,
        complete: results => {
          this.videoData = results.data.filter(item =>item.title);
          axios.get('/static/up_like_data.csv').then(response => {
            Papa.parse(response.data, {
              header: true,
              complete: results => {
                this.upData = results.data.filter(item =>item.up);
                this.drawCharts();
              },
            });
          });
        },
      });
    });
  },
};
</script>

<style scoped>
#videoBar,
#upBar {
  margin-bottom: 60px;
}
</style>
