<template>
    <el-table :data="envNotariseData">
        <el-table-column prop="projectTitle">

        </el-table-column>

        <el-table-column prop="notariseItem">

        </el-table-column>

        <el-table-column prop="notariseEvidence">

        </el-table-column>
    </el-table>
</template>

<script setup lang="ts">
import { reactive } from 'vue';

    interface EnvNotariseTable {
        projectTitle: string;
        notariseItem: string;
        notariseEvidence: boolean
    }

    const envNotariseData :EnvNotariseTable[] = reactive([])
</script>