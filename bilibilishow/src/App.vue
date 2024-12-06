<template>
  <el-container style="height: 100vh;">
    <!-- 顶部固定栏 -->
    <el-header class="app-header">
      Bilibili网站“每周必看”栏目数据分析
    </el-header>

    <!-- 主体内容容器 -->
    <el-container style="height: calc(100% - 60px);">
      <el-aside width="200px">
        <SidebarMenu @menu-click="handleMenuClick" />
      </el-aside>
      <el-main>
        <ContentDisplay :currentContent="currentContent" />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import SidebarMenu from './components/SidebarMenu.vue';
import ContentDisplay from './components/ContentDisplay.vue';

export default {
  components: { SidebarMenu, ContentDisplay },
  data() {
    return {
      currentContent: ''
    };
  },
  methods: {
    handleMenuClick(content) {
      this.currentContent = content;
    }
  }
};
</script>

<style>
body {
  margin: 0;
  font-family: 'Arial', sans-serif;
}

.app-header {
  height: 60px;
  line-height: 60px;
  font-size: 20px;
  font-weight: bold;
  color: #ffffff;
  text-align: center;
  background-color: #9dbbd8; /* Element UI 默认主题色 */
  border-bottom: 1px solid #ddd;
  position: sticky;
  top: 0;
  z-index: 1000;
}
</style>
