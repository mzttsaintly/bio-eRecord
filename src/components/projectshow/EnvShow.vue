<template>

    <nut-cell class="tableBox">

        <el-table :data="envNotariseData" :border="true" :span-method="envNotariseSpanMethod" style="width: 80%;"
            :show-header="false">
            <el-table-column prop="projectTitle">

            </el-table-column>

            <el-table-column prop="notariseItem">

            </el-table-column>

            <el-table-column prop="notariseEvidence">
                <template #default="radio">
                    <el-radio-group v-model="radio.row.notariseEvidence">
                        <el-radio :label="true">是</el-radio>
                        <el-radio :label="false">否</el-radio>
                    </el-radio-group>
                    <span> 符合要求</span>
                </template>
            </el-table-column>
        </el-table>
    </nut-cell>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import type { TableColumnCtx } from 'element-plus';

const envProps = defineProps<{
    operateInstruciton1: string;
    operateInstruciton2: string;
    differPressure: number | string;
    temperature: number | string;
    humidness: number | string;
}>()

interface EnvNotariseTable {
    projectTitle: string;
    notariseItem: string;
    notariseEvidence: boolean
}

const envNotariseData: EnvNotariseTable[] = reactive([
    { projectTitle: "文件确认", notariseItem: envProps.operateInstruciton1, notariseEvidence: true },
    { projectTitle: "文件确认", notariseItem: envProps.operateInstruciton2, notariseEvidence: true },
    { projectTitle: "环境确认", notariseItem: `洁净区对非洁净区压差${envProps.differPressure}Pa`, notariseEvidence: true },
    { projectTitle: "环境确认", notariseItem: `房间温度${envProps.temperature}℃，湿度${envProps.humidness}%RH`, notariseEvidence: true },
    { projectTitle: "环境确认", notariseItem: '生产区域已清洁', notariseEvidence: true },
    { projectTitle: "环境确认", notariseItem: '开启生物安全柜（或超净工作台）紫外，照射至少30min后关闭', notariseEvidence: true },
])



// 合并单元格用声明
interface SpanMethodProps {
    row: EnvNotariseTable
    column: TableColumnCtx<EnvNotariseTable>
    rowIndex: number
    columnIndex: number
}

const envNotariseSpanMethod = ({ row, column, rowIndex, columnIndex }: SpanMethodProps) => {
    let spanNum = 1
    if (columnIndex == 0) {
        spanNum = recursionRowSpan(row, rowIndex, envNotariseData)
    }
    return {
        rowspan: spanNum,
        colspan: 1,
    }
}

let nowRowSpan = 1

const recursionRowSpan = (row: EnvNotariseTable, rowIndex: number, data: EnvNotariseTable[]): number => {
    let num: number = 0
    // 判断上一行字段的值与当前行是否一致
    if (nowRowSpan == 1 && rowIndex > 0 && row.projectTitle === data[rowIndex - 1].projectTitle) {
        return 0
    }

    // 判断下一行字段的值与当前行是否一致
    if (rowIndex + 1 < data.length && row.projectTitle === data[rowIndex + 1].projectTitle) {
        nowRowSpan++;
        num = rowIndex + 1;
        return recursionRowSpan(data[num], num, data)
    } else {
        num = nowRowSpan;
        nowRowSpan = 1;
        return num;
    }
}
</script>

<style scoped>
.titleBox {
    justify-content: flex-start;
    font-size: large;
}

.tableBox {
    justify-content: center;
}
</style>