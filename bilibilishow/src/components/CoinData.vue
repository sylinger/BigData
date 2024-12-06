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
import { color } from 'echarts';
  
export default {
    name: 'CoinData',
    data() {
      return {
        videoData: [],
        upData: [],
      };
    },
    methods: {
      drawCharts() {
        // 处理视频数据
        const videoTitles = this.videoData.map(item => addLine(item.title));
        const videoCoins = this.videoData.map(item => parseInt(item.coin_data));
        
        // 渐变色柱状图的颜色设置
        const gradientColor = {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: '#73C9E3' }, // 顶部颜色
            { offset: 1, color: '#367BE3' }, // 底部颜色
          ],
        };
        // 视频柱状图
        const videoBarChart = echarts.init(document.getElementById('videoBar'));
        const videoBarOption = {
          title: {
            text: 'Top10投币最多的视频',
            left: 'center',
            top: '5%',
            textStyle: {
              fontSize: 26,
              fontWeight: 'bold',
              color:'#367BE3'
            },
          },
          xAxis: {
            type: 'category',
            data: videoTitles,
            axisLabel: {
              rotate: 0,
              fontSize: 12,
              color: '#333',
              interval: 0, // 强制显示所有标签
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
                <span style="color: #888;">投币数: </span>${params.value}
              </div>
            `,
          },
          series: [
            {
              data: videoCoins,
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
  
        // 处理UP主数据
        const upNames = this.upData.map(item => addLine(item.up));
        const upCoins = this.upData.map(item => parseInt(item.coin_data));
  
        // UP主柱状图
        const upBarChart = echarts.init(document.getElementById('upBar'));
        const upBarOption = {
          title: {
            text: 'Top10投币最多的UP主',
            left: 'center',
            top: '5%',
            textStyle: {
              fontSize: 26,
              fontWeight: 'bold',
              color:'#367BE3'
            },
          },
          xAxis: {
            type: 'category',
            data: upNames,
            axisLabel: {
              rotate: 0, // 不旋转
              fontSize: 12,
              color: '#333',
              interval: 0,
              formatter: value => (value.length > 10 ? value.slice(0, 10) + '...' : value),
            },
            axisLine: { lineStyle: { color: '#999' } },
          },
          yAxis: {
            type: 'value',
            axisLabel: { fontSize: 12, color: '#333' },
            splitLine: { lineStyle: { type: 'dashed', color: '#ddd' } },
          },
          tooltip: {
            trigger: 'axis',
            backgroundColor: '#fff',
            borderColor: '#ccc',
            borderWidth: 1,
            textStyle: { color: '#000' },
            formatter: params => {
              // 确保取到数组中的第一个对象
              if (params.length > 0) {
                const data = params[0];
                return `
                  <div style="text-align: left;">
                    <b>${data.name}</b><br/>
                    <span style="color: #888;">投币数: </span>${data.value}
                  </div>
                `;
              }
              return '';
            },
          },
          series: [
            {
              data: upCoins,
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
      // 获取视频数据
      axios.get('/static/video_coin_data.csv').then(response => {
        Papa.parse(response.data, {
          header: true,
          complete: results => {
            this.videoData = results.data.filter(item =>item.title);
            // 获取UP主数据
            axios.get('/static/up_coin_data.csv').then(response => {
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