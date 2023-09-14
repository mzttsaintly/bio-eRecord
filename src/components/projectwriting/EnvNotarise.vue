<template>
    <nut-cell class="tableBox">
        <el-autocomplete v-model="envVariate.operateInstruciton1" placeholder="操作规程文件名" clearable>
            <template #prepend>文件确认</template>
            <template #append><el-radio-group v-model="envNotariseData[0].notariseEvidence">
                    <el-radio :label="true">是</el-radio>
                    <el-radio :label="false">否</el-radio>
                </el-radio-group>
                <span> 符合要求</span></template>
        </el-autocomplete>
    </nut-cell>

    <nut-cell class="tableBox">
        <el-autocomplete v-model="envVariate.operateInstruciton2" placeholder="操作记录文件名" clearable>
            <template #prepend>文件确认</template>
            <template #append><el-radio-group v-model="envNotariseData[1].notariseEvidence">
                    <el-radio :label="true">是</el-radio>
                    <el-radio :label="false">否</el-radio>
                </el-radio-group>
                <span> 符合要求</span></template>
        </el-autocomplete>
    </nut-cell>

    <nut-cell class="tableBox">
        <el-input v-model="envVariate.differPressure" placeholder="洁净区压差" clearable type="number" style="width: 473px">
            <template #prepend>环境确认</template>
            <template #append>
                <el-radio-group v-model="envNotariseData[2].notariseEvidence">
                    <el-radio :label="true">是</el-radio>
                    <el-radio :label="false">否</el-radio>
                </el-radio-group>
                <span> 符合要求</span>
            </template>
            <template #suffix>
                <span>Pa</span>
            </template>
        </el-input>
    </nut-cell>

    <nut-cell class="tableBox">
        <el-input v-model="envVariate.humiture.temperature" placeholder="房间温度" clearable type="number" style="width: 473px">
            <template #prepend>环境确认</template>
            <template #append>
                <el-radio-group v-model="envNotariseData[3].notariseEvidence">
                    <el-radio :label="true">是</el-radio>
                    <el-radio :label="false">否</el-radio>
                </el-radio-group>
                <span> 符合要求</span>
            </template>
            <template #suffix>
                <span>℃</span>
            </template>
        </el-input>
    </nut-cell>

    <nut-cell class="tableBox">
        <el-input v-model="envVariate.humiture.humidness" placeholder="湿度" clearable type="number" style="width: 473px">
            <template #prepend>环境确认</template>
            <template #append>
                <el-radio-group v-model="envNotariseData[3].notariseEvidence">
                    <el-radio :label="true">是</el-radio>
                    <el-radio :label="false">否</el-radio>
                </el-radio-group>
                <span> 符合要求</span>
            </template>
            <template #suffix>
                <span>%RH</span>
            </template>
        </el-input>
    </nut-cell>

    <nut-cell class="tableBox">
        <el-input v-model="envNotariseData[4].notariseItem" placeholder="" clearable style="width: 473px">
            <template #prepend>环境确认</template>
            <template #append><el-radio-group v-model="envNotariseData[4].notariseEvidence">
                    <el-radio :label="true">是</el-radio>
                    <el-radio :label="false">否</el-radio>
                </el-radio-group>
                <span> 符合要求</span></template>
        </el-input>
    </nut-cell>

    <nut-cell class="tableBox">
        <el-input v-model="envNotariseData[5].notariseItem" placeholder="" clearable style="width: 473px">
            <template #prepend>环境确认</template>
            <template #append><el-radio-group v-model="envNotariseData[5].notariseEvidence">
                    <el-radio :label="true">是</el-radio>
                    <el-radio :label="false">否</el-radio>
                </el-radio-group>
                <span> 符合要求</span></template>
        </el-input>
    </nut-cell>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import type { TableColumnCtx } from 'element-plus';

const envVariate = reactive({
    operateInstruciton1: ref(),
    operateInstruciton2: ref(),
    differPressure: ref(),
    humiture: {
        temperature: ref(),
        humidness: ref()
    }

})

interface EnvNotariseTable {
    projectTitle: string;
    notariseItem: string;
    notariseEvidence: boolean
}

const envNotariseData: EnvNotariseTable[] = reactive([
    { projectTitle: "文件确认", notariseItem: envVariate.operateInstruciton1, notariseEvidence: true },
    { projectTitle: "文件确认", notariseItem: envVariate.operateInstruciton2, notariseEvidence: true },
    { projectTitle: "环境确认", notariseItem: envVariate.differPressure, notariseEvidence: true },
    { projectTitle: "环境确认", notariseItem: envVariate.humiture, notariseEvidence: true },
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