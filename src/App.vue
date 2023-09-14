<script setup lang="ts">
import { onMounted } from 'vue';
import { RouterView, useRouter } from 'vue-router';
import { useSideBarStore } from './stores/counter';
import headVue from './views/headVue.vue'

// 路由
const router = useRouter()

// 侧边栏状态
const sideBarState = useSideBarStore().sideBarState

// 获取当前屏幕宽度
const getWindowWidth = () => {
  return window.innerWidth
}

// 根据屏幕宽度修改侧边栏占据屏幕的百分比
const autoChangePercent = () => {
  let currentWindowWidth = getWindowWidth()
  if (currentWindowWidth <= 768) {
    useSideBarStore().changeSideBarWidth('50%')
  }

}

onMounted(() => {
  autoChangePercent()
})
</script>

<template>
  <el-row>
    <el-col :span="24">
      <headVue></headVue>
    </el-col>
    <el-col :span="24">
      <RouterView></RouterView>
    </el-col>
  </el-row>
  <!-- 弹出式侧边栏 -->
  <nut-popup class="sideBar" position="left" v-model:visible="sideBarState.show"
    :style="{ width: sideBarState.width, height: sideBarState.height }">
    <nut-side-navbar offset="30">
      <nut-side-navbar-item class="navItem" ikey="1" title="项目列表" @click="router.push({ path: '/projectShow' })"></nut-side-navbar-item>
      <nut-side-navbar-item class="navItem" ikey="2" title="物料管理" @click="router.push({ path: '/materialManagement' })"></nut-side-navbar-item>
      <nut-side-navbar-item class="navItem" ikey="3" title="设备管理" @click="router.push({ path: '/equipmentManagement' })"></nut-side-navbar-item>
      <nut-side-navbar-item class="navItem" ikey="3" title="测试组件" @click="router.push({ path: '/projetWrite' })"></nut-side-navbar-item>
    </nut-side-navbar>
  </nut-popup>
</template>

<style scoped>
.navItem:hover {
  --nut-sidenavbar-item-title-bg-color: rgb(148, 200, 243);
}
</style>
