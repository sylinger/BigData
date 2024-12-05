<template>
  <div class="menu-container">
    <el-header class="menu-header">
      数据分析可视化
    </el-header>
    <el-menu
      class="el-menu-vertical"
      @select="onSelect"
      :default-active="defaultActive"
      style="height: calc(100% - 50px); border-right: 1px solid #ddd;"
    >
      <el-menu-item v-for="item in menuItems" :key="item" :index="item">
        {{ item }}
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  props: {
    defaultActive: {
      type: String,
      default: ''
    }
  },
  emits: ['menu-click'],
  data() {
    return {
      menuItems: [
        '投币数据',
        '弹幕数据',
        '收藏数据',
        '点赞数据',
        '评论数据',
        '转发数据',
        '播放数据',
        '上榜主题数据',
        '上榜up主数据',
        '高频词',
        '统计与机器学习分析'
      ]
    };
  },
  methods: {
    onSelect(item) {
      this.$emit('menu-click', item);
    }
  }
};
</script>

<style>
.menu-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
}

.menu-header {
  height: 50px;
  line-height: 50px;
  font-size: 18px;
  font-weight: bold;
  color: #333;
  text-align: center;
  background-color: #f4f4f5;
  border-bottom: 1px solid #ddd;
}

.el-menu-vertical {
  background-color: #f9f9f9;
  padding-top: 10px;
}

.el-menu-item {
  font-size: 16px;
  color: #333;
}

.el-menu-item:hover {
  background-color: #e6f7ff;
}
</style>
