<template>
  <div>
    <div v-if="!currentContent" style="padding: 50px; text-align: center;">
      <p class="placeholder-text">请选择左侧菜单查看内容</p>
    </div>
    <div v-else>
      <component :is="currentComponent" />
    </div>
  </div>
</template>

<script>
import CoinData from './CoinData.vue';
import DanmakuData from './DanmakuData.vue';
import FavoriteData from './FavoriteData.vue';
import LikeData from './LikeData.vue';
import CommentData from './CommentData.vue';
import ShareData from './ShareData.vue';
import ViewData from './ViewData.vue';
import PopularSubjectData from './PopularSubjectData.vue';
import PopularUpData from './PopularUpData.vue';
import WordCloud from './WordCloud.vue';
import MLAnalysis from './MLAnalysis.vue';
export default {
  props: {
    currentContent: {
      type: String,
      required: true
    }
  },
  computed: {
  currentComponent() {
    switch(this.currentContent) {
      case '投币数据':
        return CoinData;
      case '弹幕数据':
        return DanmakuData;
      case '收藏数据':
        return FavoriteData;
      case '点赞数据':
        return LikeData;
      case '评论数据':
        return CommentData;
      case '转发数据':
        return ShareData;
      case '播放数据':
        return ViewData;
      case '上榜主题数据':
        return PopularSubjectData;
      case '上榜up主数据':
        return PopularUpData;
      case '高频词':
        return WordCloud;
      case '统计与机器学习分析':
        return MLAnalysis;
      default:
        return {
          template: '<p>请选择左侧菜单查看内容</p>'
        };
    }
  }
}
};
</script>

<style>
h2 {
  color: #333;
}
.placeholder-text {
  font-size: 50px; /* 字体大小 */
  color: #ff7f50; /* 字体颜色（珊瑚色） */
  font-weight: bold; /* 字体加粗 */
  font-family: 'Arial', sans-serif; /* 字体样式 */
}
</style>
