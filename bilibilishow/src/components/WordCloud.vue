<template>
  <div>
    <div id="titleWordCloud" class="word-cloud"></div>
    <div id="descWordCloud" class="word-cloud"></div>
    <div id="rcmdWordCloud" class="word-cloud"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import 'echarts-wordcloud';
import axios from 'axios';
import Papa from 'papaparse';

// 数据映射函数
function mapToList(data) {
  return data.map(item => ({
    name: item.word,
    value: parseInt(item.count, 10),
  }));
}

export default {
  name: 'WordCloud',
  data() {
    return {
      titleWords: [],
      descWords: [],
      rcmdWords: [],
    };
  },
  methods: {
    drawWordClouds() {
      const options = (title, data) => ({
        title: {
          text: title,
          left: 'center',
          textStyle: {
            fontSize: 28,
            fontWeight: 'bold',
            color: '#333',
            fontFamily: 'Arial, sans-serif',
          },
        },
        tooltip: {
          trigger: 'item',
          formatter: params => `
            <div style="text-align: left;">
              <b>${params.name}</b><br/>
              <span style="color: #888;">频率: </span>${params.value}
            </div>
          `,
        },
        series: [
          {
            type: 'wordCloud',
            shape: 'circle',
            data,
            textStyle: {
              fontFamily: 'sans-serif',
              fontWeight: 'bold',
              color: params => {
                const colors = [
                  '#FF7043', '#4CAF50', '#42A5F5', '#AB47BC', '#FFCA28',
                  '#26A69A', '#D4E157', '#EC407A', '#5C6BC0', '#FF5722',
                ];
                const baseColor = colors[Math.floor(Math.random() * colors.length)];
                const alpha = Math.min(1, params.value / 100); // 根据频率调整透明度
                return `rgba(${parseInt(baseColor.slice(1, 3), 16)}, ${parseInt(baseColor.slice(3, 5), 16)}, ${parseInt(baseColor.slice(5, 7), 16)}, ${alpha})`;
              },
            },
            sizeRange: [20, 100], // 字体大小范围
            rotationRange: [-45, 45], // 随机旋转角度
            gridSize: 8, // 单词间距
            width: '90%', // 填充宽度
            height: '80%', // 填充高度
            top: 'center',
            left: 'center',
          },
        ],
      });

      const titleChart = echarts.init(document.getElementById('titleWordCloud'));
      titleChart.setOption(options('标题常见词', mapToList(this.titleWords)));

      const descChart = echarts.init(document.getElementById('descWordCloud'));
      descChart.setOption(options('视频简介常见词', mapToList(this.descWords)));

      const rcmdChart = echarts.init(document.getElementById('rcmdWordCloud'));
      rcmdChart.setOption(options('推荐理由常见词', mapToList(this.rcmdWords)));
    },
  },
  mounted() {
    axios.get('/static/title_word.csv').then(response => {
      Papa.parse(response.data, {
        header: true,
        complete: results => {
          this.titleWords = results.data;
          axios.get('/static/desc_word.csv').then(response => {
            Papa.parse(response.data, {
              header: true,
              complete: results => {
                this.descWords = results.data;
                axios.get('/static/rcmd_reason_word.csv').then(response => {
                  Papa.parse(response.data, {
                    header: true,
                    complete: results => {
                      this.rcmdWords = results.data;
                      this.drawWordClouds();
                    },
                  });
                });
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
.word-cloud {
  width: 100%;
  height: 600px;
  margin-bottom: 60px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  border-radius: 100px;
  background: linear-gradient(135deg, #f9f9f9, #f1f1f1);
  padding: 15px;
}
</style>
