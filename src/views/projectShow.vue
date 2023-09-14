<template>
    <EnvNotarise :operateInstruciton1="op1" :operateInstruciton2="op2" :differPressure=differPressure
        :temperature="temperature" :humidness="humidness"></EnvNotarise>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import EnvNotarise from '@/components/projectshow/EnvShow.vue';

const op1 = ref('《骨髓间充质干细胞注射液制备操作流程》')
const op2 = ref('《骨髓间充质干细胞复苏培养记录》')
const differPressure = ref(10)
const temperature = ref(222)
const humidness = ref(44)
</script>