<template>
    <nut-navbar class="topNav" title="快捷记录" @on-click-back="handleClick"
        @on-click-right="router.push({ path: '/login' })">
        <template #left>
            <HorizontalN class="left" width="16px"></HorizontalN>
        </template>

        <template #right>
            <My2 class="right" width="16px"></My2>
        </template>
    </nut-navbar>
</template>

<script setup lang="ts">
import { useSideBarStore } from '../stores/counter';
import { useRouter } from 'vue-router';
import { HorizontalN, My2 } from '@nutui/icons-vue';
const router = useRouter()
// 侧边栏开关
const handleClick = useSideBarStore().handleClick
</script>

<style scoped>

</style>